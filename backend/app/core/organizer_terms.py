from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models import Organizer, OrganizerTermsAcceptance

ACTION_ACCEPTED_TERMS_OF_SERVICE = "ACCEPTED_TERMS_OF_SERVICE"
CURRENT_TOS_VERSION = "1.0"

ORGANIZER_STATUS_ACTIVE = "active"
ORGANIZER_STATUS_INACTIVE = "inactive"
ORGANIZER_STATUS_DISABLED = "disabled"

TERMS_REQUIRED_MESSAGE = (
    "Terms of service must be accepted before you can sign in."
)
ORGANIZER_DISABLED_MESSAGE = "This account has been disabled by an administrator."


def organizer_has_accepted_terms(db: Session, organizer_id: int) -> bool:
    return (
        db.query(OrganizerTermsAcceptance.id)
        .filter(OrganizerTermsAcceptance.organizer_id == organizer_id)
        .first()
        is not None
    )


def get_organizer_account_status(
    organizer: Organizer,
    *,
    has_accepted_terms: bool,
) -> str:
    if not has_accepted_terms:
        return ORGANIZER_STATUS_INACTIVE
    if organizer.is_active:
        return ORGANIZER_STATUS_ACTIVE
    return ORGANIZER_STATUS_DISABLED


def record_organizer_terms_acceptance(
    *,
    organizer: Organizer,
    db: Session,
    ip_address: str | None,
    tos_version: str = CURRENT_TOS_VERSION,
) -> OrganizerTermsAcceptance:
    acceptance = OrganizerTermsAcceptance(
        organizer_id=organizer.id,
        action=ACTION_ACCEPTED_TERMS_OF_SERVICE,
        tos_version=tos_version,
        ip_address=ip_address,
        accepted_at=datetime.now(timezone.utc),
    )
    db.add(acceptance)
    organizer.is_active = True
    return acceptance
