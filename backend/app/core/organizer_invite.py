"""
Shared logic for inviting CTCs (organizers) via email.
"""
import bcrypt
from sqlalchemy.orm import Session

from ..models import Organizer
from .email import send_organizer_credentials
from .investigators import generate_temp_password
from .security import bump_organizer_session
from .validators import normalize_email


class DuplicateOrganizerError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(
            f"A CTC with email '{email}' already exists."
        )


def organizer_exists(email: str, db: Session) -> bool:
    return (
        db.query(Organizer)
        .filter(Organizer.username == email)
        .first()
        is not None
    )


def create_and_send_organizer_invite(*, email: str, db: Session) -> Organizer:
    """
    Create a CTC account, send credential email, and flush to DB.
    Caller is responsible for commit/rollback.
    """
    email = normalize_email(email)

    if organizer_exists(email, db):
        raise DuplicateOrganizerError(email)

    temp_password = generate_temp_password()
    password_hash = bcrypt.hashpw(temp_password.encode(), bcrypt.gensalt()).decode()

    organizer = Organizer(
        username=email,
        password_hash=password_hash,
        is_active=True,
    )
    db.add(organizer)
    db.flush()

    send_organizer_credentials(
        to_email=email,
        temp_password=temp_password,
    )
    return organizer


def reset_organizer_password(*, email: str, db: Session) -> bool:
    """
    Generate a new password for an active CTC and email it.
    Returns True if a matching active account was found and email sent.
    Caller is responsible for commit/rollback.
    """
    email = normalize_email(email)

    organizer = db.query(Organizer).filter(Organizer.username == email).first()
    if not organizer or not organizer.is_active:
        return False

    temp_password = generate_temp_password()
    organizer.password_hash = bcrypt.hashpw(
        temp_password.encode(), bcrypt.gensalt()
    ).decode()
    bump_organizer_session(organizer)
    db.flush()

    send_organizer_credentials(
        to_email=email,
        temp_password=temp_password,
        is_reset=True,
    )
    return True
