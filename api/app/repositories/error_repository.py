from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import ErrorLog
from app.models.enums import ErrorLevel, ErrorSource


async def create(
    db: AsyncSession,
    *,
    source: ErrorSource,
    level: ErrorLevel,
    message: str,
    context: dict | None = None,
    stack_trace: str | None = None,
) -> ErrorLog:
    entry = ErrorLog(
        source=source, level=level, message=message, context=context or {}, stack_trace=stack_trace
    )
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    return entry


async def list_all(
    db: AsyncSession,
    *,
    source: ErrorSource | None = None,
    resolved: bool | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ErrorLog]:
    query = select(ErrorLog).order_by(ErrorLog.created_at.desc())
    if source is not None:
        query = query.where(ErrorLog.source == source)
    if resolved is not None:
        query = query.where(ErrorLog.resolved == resolved)
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all())


async def mark_resolved(db: AsyncSession, error: ErrorLog) -> ErrorLog:
    error.resolved = True
    await db.commit()
    await db.refresh(error)
    return error
