"""
core/investigators.py
Helper utilities for investigator username/password generation.
"""
import secrets

from sqlalchemy.orm import Session

from ..models import Investigator, Organizer, Study

INVESTIGATOR_CTC_DISABLED_MESSAGE = (
    "Site investigator access is unavailable because the "
    "Central Trial Coordinator (CTC) account has been disabled."
)
INVESTIGATOR_REVOKED_MESSAGE = "Investigator access has been revoked."

# Unambiguous charset — no 0/O, 1/I/L.
INVESTIGATOR_USERNAME_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
INVESTIGATOR_USERNAME_LENGTH = 6
MAX_USERNAME_ATTEMPTS = 20


def normalize_investigator_username(value: str) -> str:
    return value.strip().upper()


def generate_username(db: Session) -> str:
    """
    Return a random alphanumeric username globally unique across all investigators.
    Example: "K7M2P9", "R3H8WN".
    """
    for _ in range(MAX_USERNAME_ATTEMPTS):
        username = "".join(
            secrets.choice(INVESTIGATOR_USERNAME_ALPHABET)
            for _ in range(INVESTIGATOR_USERNAME_LENGTH)
        )
        exists = (
            db.query(Investigator.id)
            .filter(Investigator.username == username)
            .first()
        )
        if not exists:
            return username
    raise RuntimeError("Could not generate a unique investigator username.")


def organizer_for_investigator(db: Session, investigator: Investigator) -> Organizer | None:
    return (
        db.query(Organizer)
        .join(Study, Study.organizer_id == Organizer.id)
        .filter(Study.id == investigator.study_id)
        .first()
    )


def investigator_ctc_is_active(db: Session, investigator: Investigator) -> bool:
    organizer = organizer_for_investigator(db, investigator)
    return organizer is not None and organizer.is_active


def invalidate_investigator_sessions_for_organizer(db: Session, organizer_id: int) -> None:
    investigators = (
        db.query(Investigator)
        .join(Study, Investigator.study_id == Study.id)
        .filter(Study.organizer_id == organizer_id)
        .all()
    )
    for investigator in investigators:
        investigator.session_version += 1


def generate_temp_password() -> str:
    """
    Generate a random temporary password (URL-safe base64, ~16 printable chars).
    Long enough to be secure, short enough to type from an email.
    """
    return secrets.token_urlsafe(12)  # → 16-char URL-safe string
