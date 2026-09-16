import json
import logging
import smtplib
import urllib.error
import urllib.request
from email.message import EmailMessage

from ..config import (
    FRONTEND_URL,
    IS_PRODUCTION,
    RESEND_API_KEY,
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_USE_TLS,
    SMTP_USER,
    email_is_configured,
)

logger = logging.getLogger(__name__)


def _send_via_resend(to: str, subject: str, body: str) -> None:
    """Send email using Resend's HTTP API (avoids outbound SMTP port blocks)."""
    payload = json.dumps({
        "from": SMTP_FROM,
        "to": [to],
        "subject": subject,
        "text": body,
    }).encode()

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "resend-python/2.0.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status not in (200, 201):
                raise RuntimeError(f"Resend API returned status {resp.status}")
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode(errors="replace")
        logger.error("Resend API error %s: %s", exc.code, body_text)
        raise RuntimeError(f"Resend API error {exc.code}: {body_text}") from exc


def _send_via_smtp(to: str, subject: str, body: str) -> None:
    """Send email via SMTP (port 465 = SSL, port 587 = STARTTLS)."""
    message = EmailMessage()
    message["From"] = SMTP_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    use_ssl = SMTP_PORT == 465
    if use_ssl:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            if SMTP_USER and SMTP_PASSWORD:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)
    else:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            if SMTP_USE_TLS:
                server.starttls()
            if SMTP_USER and SMTP_PASSWORD:
                server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(message)


def send_email(to: str, subject: str, body: str) -> None:
    if not email_is_configured():
        if IS_PRODUCTION:
            raise RuntimeError("Email service is not configured.")
        logger.warning(
            "Email not configured — would send to %s | subject: %s\n%s",
            to,
            subject,
            body,
        )
        return

    try:
        if RESEND_API_KEY:
            # Preferred on Railway — HTTP API bypasses SMTP port restrictions.
            _send_via_resend(to, subject, body)
        else:
            _send_via_smtp(to, subject, body)
    except Exception as exc:
        logger.error("Failed to send email to %s: %s", to, exc)
        raise RuntimeError(f"Failed to send email: {exc}") from exc


def send_investigator_credentials(
    to_email: str,
    name: str | None,
    study_title: str,
    protocol_code: str,
    username: str,
    temp_password: str,
    *,
    is_reset: bool = False,
) -> None:
    login_url = f"{FRONTEND_URL.rstrip('/')}/investigator/login"
    greeting = name.strip() if name and name.strip() else "Investigator"

    if is_reset:
        subject = f"Your new investigator password for study: {study_title}"
        intro = "A new password was requested for your Study Randomizer investigator account."
    else:
        subject = f"Your investigator credentials for study: {study_title}"
        intro = "You have been added as an investigator on a clinical study on Study Randomizer."

    body = f"""Hello {greeting},

{intro}

Study: {study_title}
Protocol: {protocol_code.strip()}

Your login credentials:
  Username : {username}
  Password : {temp_password}

Login at: {login_url}

Open the link above to sign in.
You can change your password after logging in.

If you did not expect this email, please contact the study organizer.

— Study Randomizer
"""

    send_email(to_email, subject, body)


def send_organizer_credentials(
    to_email: str,
    temp_password: str,
    *,
    is_reset: bool = False,
) -> None:
    login_url = f"{FRONTEND_URL.rstrip('/')}/organizer/login"

    if is_reset:
        subject = "Your new CTC password for Study Randomizer"
        intro = "A new password was requested for your Central Trial Coordinator (CTC) account on Study Randomizer."
    else:
        subject = "Your CTC credentials for Study Randomizer"
        intro = "You have been invited as a Central Trial Coordinator (CTC) on Study Randomizer."

    body = f"""Hello,

{intro}

Your login credentials:
  Email    : {to_email}
  Password : {temp_password}

Login at: {login_url}

You can change your password after logging in.

If you did not request this, please contact your system administrator.

— Study Randomizer
"""

    send_email(to_email, subject, body)


def send_unblind_notification(
    to_email: str,
    *,
    study_title: str,
    protocol_code: str,
    investigator_username: str,
    investigator_email: str,
    investigator_name: str | None,
    patient_id: str,
    kit_code: str,
    treatment_name: str,
) -> None:
    subject = f"Emergency unblinding alert — {study_title}"
    name_line = (
        f"  Name     : {investigator_name.strip()}\n"
        if investigator_name and investigator_name.strip()
        else ""
    )

    body = f"""Hello,

An investigator has performed an emergency unblinding on a study assignment.

Study: {study_title}
Protocol: {protocol_code.strip()}

Investigator:
  Username : {investigator_username}
  Email    : {investigator_email}
{name_line}
Assignment:
  Patient ID    : {patient_id}
  Kit Code      : {kit_code}
  Treatment Arm : {treatment_name}

This event has been recorded in the audit log.

— Study Randomizer
"""

    send_email(to_email, subject, body)
