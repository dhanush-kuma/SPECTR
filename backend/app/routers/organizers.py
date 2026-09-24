from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..core.audit import audit
from ..core.organizer_invite import (
    DuplicateOrganizerError,
    create_and_send_organizer_invite,
)
from ..core.investigators import invalidate_investigator_sessions_for_organizer
from ..core.organizer_stats import (
    get_organizer_terms_accepted_at,
    get_organizer_usage_stats,
    get_study_summaries_for_organizer,
)
from ..core.organizer_terms import (
    get_organizer_account_status,
    organizer_has_accepted_terms,
)
from ..core.rate_limit import limiter
from ..core.security import bump_organizer_session, get_current_admin
from ..database import get_db
from ..models import Admin, Organizer
from ..schemas import (
    AdminStudySummaryOut,
    InviteOrganizerRequest,
    OrganizerDetailOut,
    OrganizerOut,
    OrganizerSummaryOut,
    UpdateOrganizerCountsRequest,
)

router = APIRouter(prefix="/admin/organizers", tags=["organizers"])


def _organizer_out(organizer: Organizer, db: Session) -> OrganizerOut:
    has_accepted_terms = organizer_has_accepted_terms(db, organizer.id)
    return OrganizerOut(
        id=organizer.id,
        username=organizer.username,
        is_active=organizer.is_active,
        status=get_organizer_account_status(
            organizer,
            has_accepted_terms=has_accepted_terms,
        ),
    )


def _organizer_summary_out(organizer: Organizer, db: Session) -> OrganizerSummaryOut:
    has_accepted_terms = organizer_has_accepted_terms(db, organizer.id)
    stats = get_organizer_usage_stats(db, organizer.id)
    return OrganizerSummaryOut(
        id=organizer.id,
        username=organizer.username,
        is_active=organizer.is_active,
        status=get_organizer_account_status(
            organizer,
            has_accepted_terms=has_accepted_terms,
        ),
        created_at=organizer.created_at,
        **stats,
        study_count_limit=organizer.study_count,
        records_per_study_limit=organizer.records_count,
    )


def _get_organizer_or_404(organizer_id: int, db: Session) -> Organizer:
    organizer = db.query(Organizer).filter(Organizer.id == organizer_id).first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found.")
    return organizer


@router.post("/", response_model=OrganizerOut, status_code=201)
@limiter.limit("20/hour")
def invite_organizer(
    request: Request,
    payload: InviteOrganizerRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    try:
        organizer = create_and_send_organizer_invite(
            email=payload.email,
            db=db,
        )
    except DuplicateOrganizerError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except RuntimeError as exc:
        db.rollback()
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    db.commit()
    db.refresh(organizer)
    audit(
        "organizer.invited",
        organizer=organizer.username,
        admin=current_admin.username,
    )
    return _organizer_out(organizer, db)


@router.get("/", response_model=list[OrganizerSummaryOut])
def list_organizers(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    organizers = db.query(Organizer).order_by(Organizer.created_at.desc()).all()
    return [_organizer_summary_out(organizer, db) for organizer in organizers]


@router.get("/{organizer_id}", response_model=OrganizerDetailOut)
def get_organizer_detail(
    organizer_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    organizer = _get_organizer_or_404(organizer_id, db)
    summary = _organizer_summary_out(organizer, db)
    return OrganizerDetailOut(
        **summary.model_dump(),
        terms_accepted_at=get_organizer_terms_accepted_at(db, organizer.id),
    )


@router.get("/{organizer_id}/studies", response_model=list[AdminStudySummaryOut])
def get_organizer_studies(
    organizer_id: int,
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    _get_organizer_or_404(organizer_id, db)
    summaries = get_study_summaries_for_organizer(db, organizer_id)
    return [AdminStudySummaryOut(**summary) for summary in summaries]


@router.patch("/{organizer_id}/counts", response_model=OrganizerDetailOut)
@limiter.limit("30/hour")
def update_organizer_counts(
    request: Request,
    organizer_id: int,
    payload: UpdateOrganizerCountsRequest,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    organizer = _get_organizer_or_404(organizer_id, db)
    organizer.study_count = payload.study_count
    organizer.records_count = payload.records_count
    db.commit()
    db.refresh(organizer)
    audit(
        "organizer.counts_updated",
        organizer=organizer.username,
        study_count=payload.study_count,
        records_count=payload.records_count,
        admin=current_admin.username,
    )
    summary = _organizer_summary_out(organizer, db)
    return OrganizerDetailOut(
        **summary.model_dump(),
        terms_accepted_at=get_organizer_terms_accepted_at(db, organizer.id),
    )


@router.patch("/{organizer_id}/status", response_model=OrganizerOut)
@limiter.limit("30/hour")
def toggle_organizer_status(
    request: Request,
    organizer_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    organizer = _get_organizer_or_404(organizer_id, db)

    organizer.is_active = not organizer.is_active
    if not organizer.is_active:
        bump_organizer_session(organizer)
        invalidate_investigator_sessions_for_organizer(db, organizer.id)
    db.commit()
    db.refresh(organizer)
    audit(
        "organizer.status_changed",
        organizer=organizer.username,
        is_active=organizer.is_active,
        admin=current_admin.username,
    )
    return _organizer_out(organizer, db)
