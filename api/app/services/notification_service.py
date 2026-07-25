import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AdminRole, NotificationCategory, NotificationSeverity
from app.repositories import notification_repository

logger = logging.getLogger("app.notifications")


async def notify(
    db: AsyncSession,
    *,
    category: NotificationCategory,
    title: str,
    message: str,
    audience_min_role: AdminRole,
    severity: NotificationSeverity = NotificationSeverity.info,
    related_type: str | None = None,
    related_id: str | None = None,
) -> None:
    """Cree une notification in-app. Ne doit jamais interrompre le flux appelant :
    une erreur ici (ex. probleme transitoire de connexion) est seulement loggee."""
    try:
        await notification_repository.create(
            db,
            category=category,
            severity=severity,
            title=title,
            message=message,
            audience_min_role=audience_min_role,
            related_type=related_type,
            related_id=related_id,
        )
    except Exception:  # noqa: BLE001
        logger.exception("Echec de creation de notification (categorie=%s, titre=%s)", category, title)
