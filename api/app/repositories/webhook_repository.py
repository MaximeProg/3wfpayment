import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import WebhookEventStatus
from app.models.webhook import WebhookEvent


async def get_by_external_event_id(db: AsyncSession, external_event_id: str) -> WebhookEvent | None:
    result = await db.execute(
        select(WebhookEvent).where(WebhookEvent.external_event_id == external_event_id)
    )
    return result.scalar_one_or_none()


async def create(
    db: AsyncSession,
    *,
    event_type: str,
    external_event_id: str,
    signature_valid: bool,
    raw_payload: dict,
) -> WebhookEvent:
    event = WebhookEvent(
        event_type=event_type,
        external_event_id=external_event_id,
        signature_valid=signature_valid,
        raw_payload=raw_payload,
        status=WebhookEventStatus.received,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def mark_processed(
    db: AsyncSession, event: WebhookEvent, *, transaction_id: uuid.UUID
) -> WebhookEvent:
    event.status = WebhookEventStatus.processed
    event.transaction_id = transaction_id
    event.processed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(event)
    return event


async def mark_failed(db: AsyncSession, event: WebhookEvent, *, error: str) -> WebhookEvent:
    event.status = WebhookEventStatus.failed
    event.processing_error = error
    event.processed_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(event)
    return event


async def get_by_id(db: AsyncSession, event_id: uuid.UUID) -> WebhookEvent | None:
    return await db.get(WebhookEvent, event_id)


async def list_events(
    db: AsyncSession, *, status: WebhookEventStatus | None = None, limit: int = 50, offset: int = 0
) -> list[WebhookEvent]:
    query = select(WebhookEvent).order_by(WebhookEvent.received_at.desc())
    if status is not None:
        query = query.where(WebhookEvent.status == status)
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    return list(result.scalars().all())
