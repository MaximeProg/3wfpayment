import logging

import resend

from app.core.config import get_settings

logger = logging.getLogger("app.email")

settings = get_settings()
resend.api_key = settings.resend_api_key


def send_email(*, to: str | list[str], subject: str, html: str, text: str | None = None) -> str | None:
    """Envoie un email via Resend. Retourne l'id du message, ou None si l'envoi est desactive
    (pas de cle configuree en environnement de developpement)."""
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY absent - email non envoye (sujet=%s, to=%s)", subject, to)
        return None

    params: resend.Emails.SendParams = {
        "from": settings.resend_from_email,
        "to": to if isinstance(to, list) else [to],
        "subject": subject,
        "html": html,
    }
    if text:
        params["text"] = text

    try:
        email = resend.Emails.send(params)
    except Exception:
        logger.exception("Echec d'envoi d'email via Resend (sujet=%s, to=%s)", subject, to)
        return None
    return email.get("id")
