from datetime import datetime, timezone
import bcrypt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import clear_auth_cookie, clear_csrf_cookie, set_auth_cookie, set_csrf_cookie
from ..core.audit import audit
from ..core.rate_limit import limiter
from ..core.study_status import ACTIVE, COMPLETE, GENERATED
from ..core.security import (
    ROLE_INVESTIGATOR,
    bump_investigator_session,
    cookie_max_age_for_access_token,
    create_access_token,
    get_current_investigator,
    remember_me_from_access_token,
    revoke_token,
)
from ..database import get_db
from ..models import Investigator, RandomizationRecord, Site, Strata, Study
from ..schemas import (
    AssignKitRequest,
    ChangePasswordRequest,
    InvestigatorInfo,
    InvestigatorLoginRequest,
    LoginResponse,
    MessageResponse,
    RandomizationRecordOut,
    StrataAvailabilityOut,
    UnblindResponse,
)

router = APIRouter(prefix="/investigator", tags=["investigator"])

COOKIE_NAME = "investigator_access_token"


def _investigator_record_out(
    record: RandomizationRecord,
    investigator_username: str | None = None,
) -> RandomizationRecordOut:
    """Hide treatment arm while the record is still blinded."""
    return RandomizationRecordOut(
        id=record.id,
        study_id=record.study_id,
        sequence_number=record.sequence_number,
        kit_code=record.kit_code,
        treatment_name=record.treatment_name if not record.blind else None,
        assigned_patient_id=record.assigned_patient_id,
        assigned_by_investigator_id=record.assigned_by_investigator_id,
        assigned_by_investigator_username=investigator_username,
        assigned_at=record.assigned_at,
        blind=record.blind,
    )


@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
def login(
    request: Request,
    payload: InvestigatorLoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    # Resolve the study by trial_id (= protocol_code)
    study = db.query(Study).filter(Study.protocol_code == payload.trial_id.strip()).first()
    if not study:
        audit(
            "investigator.login.failed",
            trial_id=payload.trial_id,
            reason="study_not_found",
            ip=request.client.host if request.client else None,
        )
        raise HTTPException(status_code=401, detail="Invalid trial ID, username, or password.")

    # Find the investigator by (study_id, username) — username is unique within a study
    investigator = (
        db.query(Investigator)
        .filter(
            Investigator.study_id == study.id,
            Investigator.username == payload.username.strip(),
        )
        .first()
    )

    if not investigator or not bcrypt.checkpw(
        payload.password.encode(), investigator.password_hash.encode()
    ):
        audit(
            "investigator.login.failed",
            trial_id=payload.trial_id,
            username=payload.username,
            ip=request.client.host if request.client else None,
        )
        raise HTTPException(status_code=401, detail="Invalid trial ID, username, or password.")

    if investigator.status == "revoked":
        audit(
            "investigator.login.failed",
            trial_id=payload.trial_id,
            username=payload.username,
            reason="revoked",
            ip=request.client.host if request.client else None,
        )
        raise HTTPException(status_code=401, detail="Your access to this study has been revoked.")

    # Promote inactive → active on first login
    if investigator.status == "inactive":
        investigator.status = "active"
        db.commit()

    # JWT sub stores the investigator's DB id (study-unique usernames would collide across studies)
    remember_me = payload.remember_me
    token = create_access_token(
        str(investigator.id),
        ROLE_INVESTIGATOR,
        session_version=investigator.session_version,
        remember_me=remember_me,
    )
    cookie_max_age = cookie_max_age_for_access_token(token)
    set_auth_cookie(response, COOKIE_NAME, token, cookie_max_age)
    csrf_token = set_csrf_cookie(response, cookie_max_age)
    audit(
        "investigator.login.success",
        investigator_id=investigator.id,
        trial_id=payload.trial_id,
        username=investigator.username,
        ip=request.client.host if request.client else None,
    )
    return LoginResponse(message="Login successful.", csrf_token=csrf_token)


@router.post("/logout", response_model=MessageResponse)
def logout(
    response: Response,
    investigator_access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
    current_investigator: Investigator = Depends(get_current_investigator),
):
    revoke_token(investigator_access_token, db)
    clear_auth_cookie(response, COOKIE_NAME)
    clear_csrf_cookie(response)
    audit("investigator.logout", investigator_id=current_investigator.id)
    return MessageResponse(message="Logged out successfully.")


@router.get("/me", response_model=InvestigatorInfo)
def get_me(
    response: Response,
    investigator_access_token: str | None = Cookie(default=None),
    current_investigator: Investigator = Depends(get_current_investigator),
    db: Session = Depends(get_db),
):
    study = db.query(Study).filter(Study.id == current_investigator.study_id).first()
    site = None
    if current_investigator.site_id:
        site = db.query(Site).filter(Site.id == current_investigator.site_id).first()
    cookie_max_age = cookie_max_age_for_access_token(investigator_access_token)
    csrf_token = set_csrf_cookie(response, cookie_max_age)
    return InvestigatorInfo(
        id=current_investigator.id,
        username=current_investigator.username,
        email=current_investigator.email,
        name=current_investigator.name,
        study_id=current_investigator.study_id,
        site_id=current_investigator.site_id,
        site_name=site.name if site else None,
        trial_id=study.protocol_code if study else "",
        study_title=study.title if study else None,
        study_description=study.description if study else None,
        blinding_type=study.blinding_type if study else "Double-Blind",
        emergency_unblinding_allowed=study.emergency_unblinding_allowed if study else True,
        status=current_investigator.status,
        csrf_token=csrf_token,
    )


@router.post("/change-password", response_model=LoginResponse)
@limiter.limit("5/minute")
def change_password(
    request: Request,
    payload: ChangePasswordRequest,
    response: Response,
    investigator_access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
    current_investigator: Investigator = Depends(get_current_investigator),
):
    if not bcrypt.checkpw(
        payload.current_password.encode(), current_investigator.password_hash.encode()
    ):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")

    bump_investigator_session(current_investigator)
    current_investigator.password_hash = bcrypt.hashpw(
        payload.new_password.encode(), bcrypt.gensalt()
    ).decode()
    revoke_token(investigator_access_token, db)
    db.commit()
    db.refresh(current_investigator)

    remember_me = remember_me_from_access_token(investigator_access_token)
    token = create_access_token(
        str(current_investigator.id),
        ROLE_INVESTIGATOR,
        session_version=current_investigator.session_version,
        remember_me=remember_me,
    )
    cookie_max_age = cookie_max_age_for_access_token(token)
    set_auth_cookie(response, COOKIE_NAME, token, cookie_max_age)
    csrf_token = set_csrf_cookie(response, cookie_max_age)
    audit("investigator.password_changed", investigator_id=current_investigator.id)
    return LoginResponse(message="Password changed successfully.", csrf_token=csrf_token)


@router.get("/strata-availability", response_model=list[StrataAvailabilityOut])
def get_strata_availability(
    db: Session = Depends(get_db),
    current_investigator: Investigator = Depends(get_current_investigator),
):
    """Unassigned randomization counts per stratum at the investigator's site."""
    if current_investigator.site_id is None:
        return []

    stratas = (
        db.query(Strata)
        .filter(Strata.site_id == current_investigator.site_id)
        .order_by(Strata.name.asc())
        .all()
    )

    availability: list[StrataAvailabilityOut] = []
    for strata in stratas:
        unassigned_count = (
            db.query(RandomizationRecord)
            .filter(
                RandomizationRecord.site_id == current_investigator.site_id,
                RandomizationRecord.strata_id == strata.id,
                RandomizationRecord.assigned_patient_id.is_(None),
            )
            .count()
        )
        availability.append(
            StrataAvailabilityOut(
                id=strata.id,
                name=strata.name,
                unassigned_count=unassigned_count,
            )
        )

    return availability


@router.post("/assign-kit", response_model=RandomizationRecordOut)
@limiter.limit("30/minute")
def assign_kit(
    request: Request,
    payload: AssignKitRequest,
    db: Session = Depends(get_db),
    current_investigator: Investigator = Depends(get_current_investigator),
):
    patient_id = payload.patient_id.strip()
    if not patient_id:
        raise HTTPException(status_code=400, detail="Patient ID is required.")

    study_id = current_investigator.study_id
    if current_investigator.site_id is None:
        raise HTTPException(
            status_code=400,
            detail="Your account is not linked to a site. Contact the study coordinator.",
        )

    study = db.query(Study).filter(Study.id == study_id).first()
    if not study:
        raise HTTPException(status_code=404, detail="Study not found.")

    strata = (
        db.query(Strata)
        .filter(
            Strata.id == payload.strata_id,
            Strata.site_id == current_investigator.site_id,
            Strata.study_id == study_id,
        )
        .first()
    )
    if not strata:
        raise HTTPException(
            status_code=400,
            detail="Invalid stratum selection for your site.",
        )

    try:
        existing = (
            db.query(RandomizationRecord)
            .filter(
                RandomizationRecord.study_id == study_id,
                func.lower(RandomizationRecord.assigned_patient_id) == patient_id.lower(),
            )
            .with_for_update()
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=409,
                detail=f"Patient ID '{patient_id}' has already been assigned a kit code in this study.",
            )

        record = (
            db.query(RandomizationRecord)
            .filter(
                RandomizationRecord.study_id == study_id,
                RandomizationRecord.site_id == current_investigator.site_id,
                RandomizationRecord.strata_id == payload.strata_id,
                RandomizationRecord.assigned_patient_id.is_(None),
            )
            .order_by(RandomizationRecord.sequence_number.asc())
            .with_for_update()
            .first()
        )
        if not record:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"No unassigned kit codes remaining for stratum "
                    f"'{strata.name}' at this site."
                ),
            )

        record.assigned_patient_id = patient_id
        record.assigned_by_investigator_id = current_investigator.id
        record.assigned_at = datetime.now(timezone.utc)

        if study.status == GENERATED:
            study.status = ACTIVE

        # Session uses autoflush=False — flush so the count sees this assignment.
        db.flush()

        remaining_unassigned = (
            db.query(RandomizationRecord)
            .filter(
                RandomizationRecord.study_id == study_id,
                RandomizationRecord.assigned_patient_id.is_(None),
            )
            .count()
        )
        if remaining_unassigned == 0 and study.status == ACTIVE:
            study.status = COMPLETE

        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Patient ID '{patient_id}' has already been assigned a kit code in this study.",
        ) from None
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while assigning the kit code.",
        )

    db.refresh(record)
    db.refresh(study)

    audit(
        "investigator.kit_assigned",
        investigator_id=current_investigator.id,
        study_id=study_id,
        site_id=current_investigator.site_id,
        strata_id=payload.strata_id,
        patient_id=patient_id,
        kit_code=record.kit_code,
        sequence_number=record.sequence_number,
        study_status=study.status,
        ip=request.client.host if request.client else None,
    )

    return _investigator_record_out(record, current_investigator.username)


@router.get("/assignments", response_model=list[RandomizationRecordOut])
def get_assignments(
    db: Session = Depends(get_db),
    current_investigator: Investigator = Depends(get_current_investigator),
):
    records = (
        db.query(RandomizationRecord)
        .filter(
            RandomizationRecord.study_id == current_investigator.study_id,
            RandomizationRecord.assigned_by_investigator_id == current_investigator.id,
            RandomizationRecord.assigned_patient_id.isnot(None),
        )
        .order_by(RandomizationRecord.assigned_at.desc())
        .all()
    )
    res = []
    for r in records:
        username = r.assigned_by_investigator.username if r.assigned_by_investigator else None
        res.append(_investigator_record_out(r, username))
    return res


@router.post("/records/{record_id}/unblind", response_model=UnblindResponse)
def unblind_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_investigator: Investigator = Depends(get_current_investigator),
):
    record = (
        db.query(RandomizationRecord)
        .filter(
            RandomizationRecord.id == record_id,
            RandomizationRecord.study_id == current_investigator.study_id,
            RandomizationRecord.assigned_by_investigator_id == current_investigator.id,
        )
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Assigned record not found.")

    study = db.query(Study).filter(Study.id == current_investigator.study_id).first()
    if not study or not study.emergency_unblinding_allowed:
        raise HTTPException(
            status_code=403,
            detail="Emergency unblinding is disabled for this study.",
        )

    record.blind = False
    db.commit()
    db.refresh(record)

    audit(
        "investigator.emergency_unblinded",
        investigator_id=current_investigator.id,
        study_id=study.id,
        record_id=record.id,
        patient_id=record.assigned_patient_id,
        treatment_name=record.treatment_name,
    )

    return UnblindResponse(
        record_id=record.id,
        treatment_name=record.treatment_name,
        message="Patient treatment arm unblinded successfully.",
    )


