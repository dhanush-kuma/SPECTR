from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..core.audit import audit
from ..core.organizer_invite import (
    DuplicateOrganizerError,
    create_and_send_organizer_invite,
)
from ..core.rate_limit import limiter
from ..core.security import get_current_admin
from ..database import get_db
from ..models import Admin, Organizer
from ..schemas import InviteOrganizerRequest, OrganizerOut

router = APIRouter(prefix="/admin/organizers", tags=["organizers"])


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
        email=organizer.email,
        admin=current_admin.username,
    )
    return organizer


@router.get("/", response_model=list[OrganizerOut])
def list_organizers(
    db: Session = Depends(get_db),
    _: Admin = Depends(get_current_admin),
):
    return db.query(Organizer).order_by(Organizer.created_at.desc()).all()


@router.patch("/{organizer_id}/status", response_model=OrganizerOut)
def toggle_organizer_status(
    organizer_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
):
    organizer = db.query(Organizer).filter(Organizer.id == organizer_id).first()
    if not organizer:
        raise HTTPException(status_code=404, detail="Organizer not found.")

    organizer.is_active = not organizer.is_active
    db.commit()
    db.refresh(organizer)
    audit(
        "organizer.status_changed",
        organizer=organizer.username,
        is_active=organizer.is_active,
        admin=current_admin.username,
    )
    return organizer
