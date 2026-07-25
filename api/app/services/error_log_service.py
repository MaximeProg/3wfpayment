import traceback

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AdminRole, ErrorLevel, ErrorSource, NotificationCategory, NotificationSeverity
from app.repositories import error_repository
from app.services.notification_service import notify

_NOTIFY_SEVERITY = {
    ErrorLevel.warning: NotificationSeverity.warning,
    ErrorLevel.error: NotificationSeverity.critical,
    ErrorLevel.critical: NotificationSeverity.critical,
}


async def log_error(
    db: AsyncSession,
    *,
    source: ErrorSource,
    level: ErrorLevel,
    message: str,
    context: dict | None = None,
    exc: Exception | None = None,
) -> None:
    stack_trace = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)) if exc else None
    await error_repository.create(
        db, source=source, level=level, message=message, context=context, stack_trace=stack_trace
    )

    if level in (ErrorLevel.error, ErrorLevel.critical):
        await notify(
            db,
            category=NotificationCategory.error,
            severity=_NOTIFY_SEVERITY[level],
            audience_min_role=AdminRole.admin,
            title=message[:120],
            message=f"Source : {source.value}",
            related_type="error_log",
        )
