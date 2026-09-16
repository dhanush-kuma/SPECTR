import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Cookie, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..config import JWT_AUDIENCE, JWT_ISSUER, SECRET_KEY
from ..database import get_db
from ..models import Admin, Investigator, Organizer, RevokedToken

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24
REMEMBER_ME_DAYS = 30
REMEMBER_ME_MAX_AGE_SECONDS = REMEMBER_ME_DAYS * 24 * 60 * 60
ROLE_ADMIN = "admin"
ROLE_ORGANIZER = "organizer"
ROLE_INVESTIGATOR = "investigator"


def create_access_token(
    username: str,
    role: str,
    *,
    session_version: int | None = None,
    remember_me: bool = False,
) -> str:
    if role == ROLE_ADMIN:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    elif remember_me:
        expire = datetime.now(timezone.utc) + timedelta(days=REMEMBER_ME_DAYS)
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": username,
        "role": role,
        "jti": str(uuid.uuid4()),
        "exp": expire,
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
    }
    if role in (ROLE_ORGANIZER, ROLE_INVESTIGATOR):
        payload["rm"] = remember_me
    if session_version is not None:
        payload["sv"] = session_version
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def cookie_max_age_for_access_token(access_token: str | None) -> int | None:
    """Persistent cookie max-age from JWT; None means browser session cookie."""
    if not access_token:
        return None
    payload = decode_token(access_token)
    if not payload:
        return None
    role = payload.get("role")
    if role == ROLE_ADMIN:
        return None
    if payload.get("rm"):
        return REMEMBER_ME_MAX_AGE_SECONDS
    return None


def remember_me_from_access_token(access_token: str | None) -> bool:
    payload = decode_token(access_token) if access_token else None
    return bool(payload and payload.get("rm"))


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )
    except JWTError:
        return None


def purge_expired_revoked_tokens(db: Session) -> None:
    now = datetime.now(timezone.utc)
    db.query(RevokedToken).filter(RevokedToken.expires_at < now).delete()


def is_token_revoked(jti: str, db: Session) -> bool:
    return db.query(RevokedToken).filter(RevokedToken.jti == jti).first() is not None


def revoke_token(token: str | None, db: Session) -> None:
    if not token:
        return
    payload = decode_token(token)
    if not payload:
        return
    jti = payload.get("jti")
    exp = payload.get("exp")
    if not jti or not exp:
        return
    if is_token_revoked(jti, db):
        return
    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
    purge_expired_revoked_tokens(db)
    db.add(RevokedToken(jti=jti, expires_at=expires_at))
    db.commit()


def _resolve_user(
    token: str | None,
    expected_role: str,
    db: Session,
) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    if payload.get("role") != expected_role:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    jti = payload.get("jti")
    if not jti or is_token_revoked(jti, db):
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return {"username": username}


def get_current_admin(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> Admin:
    user = _resolve_user(access_token, ROLE_ADMIN, db)
    admin = db.query(Admin).filter(Admin.username == user["username"]).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found.")
    return admin


def get_current_organizer(
    organizer_access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> Organizer:
    user = _resolve_user(organizer_access_token, ROLE_ORGANIZER, db)
    organizer = (
        db.query(Organizer).filter(Organizer.username == user["username"]).first()
    )
    if not organizer:
        raise HTTPException(status_code=401, detail="Organizer not found.")
    if not organizer.is_active:
        raise HTTPException(status_code=401, detail="Organizer account is deactivated.")

    payload = decode_token(organizer_access_token) if organizer_access_token else None
    token_session_version = payload.get("sv") if payload else None
    if token_session_version is None or token_session_version != organizer.session_version:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    return organizer


def get_current_investigator(
    investigator_access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> Investigator:
    """
    Resolve the currently authenticated investigator from the session cookie.
    The JWT `sub` stores the investigator's database id (as a string).
    """
    user = _resolve_user(investigator_access_token, ROLE_INVESTIGATOR, db)
    try:
        investigator_id = int(user["username"])
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid or expired token.") from None

    payload = decode_token(investigator_access_token) if investigator_access_token else None
    token_session_version = payload.get("sv") if payload else None

    investigator = db.query(Investigator).filter(Investigator.id == investigator_id).first()
    if not investigator:
        raise HTTPException(status_code=401, detail="Investigator not found.")
    if token_session_version is None or token_session_version != investigator.session_version:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    if investigator.status == "revoked":
        raise HTTPException(status_code=401, detail="Investigator access has been revoked.")
    return investigator


def bump_investigator_session(investigator: Investigator) -> None:
    """Invalidate all outstanding investigator JWTs."""
    investigator.session_version += 1


def bump_organizer_session(organizer: Organizer) -> None:
    """Invalidate all outstanding organizer JWTs."""
    organizer.session_version += 1
