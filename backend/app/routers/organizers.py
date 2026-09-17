from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..core.audit import audit
from ..core.organizer_invite import (
    DuplicateOrganizerError,
    create_and_send_organizer_invite,
)
from ..core.organizer_terms import (
    get_organizer_account_status,
    organizer_has_accepted_terms,
)
from ..core.rate_limit import limiter
from ..core.security import bump_organizer_session, get_current_admin
from ..database import get_db
from ..models import Admin, Organizer
from ..schemas import InviteOrganizerRequest, OrganizerOut

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


@router.get("/", response_model=list[OrganizerOut])
def list_organizers(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    organizers = db.query(Organizer).order_by(Organizer.created_at.desc()).all()
    return [_organizer_out(organizer, db) for organizer in organizers]


@router.patch("/{organizer_id}/status", response_model=OrganizerOut)
@limiter.limit("30/hour")
def toggle_organizer_status(
    request: Request,
    organizer_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    organizer = db.query(Organizer).filter(Organizer.id == organizer_id).first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found.")

    organizer.is_active = not organizer.is_active
    if not organizer.is_active:
        bump_organizer_session(organizer)
    db.commit()
    db.refresh(organizer)
    audit(
        "organizer.status_changed",
        organizer=organizer.username,
        is_active=organizer.is_active,
        admin=current_admin.username,
    )
    return _organizer_out(organizer, db)
