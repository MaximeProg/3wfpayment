import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole, AuditActorType, WebhookEventStatus
from app.repositories import audit_repository
from app.repositories import webhook_repository as repo
from app.schemas.admin import WebhookEventDetailOut, WebhookEventOut
from app.services.webhook_processing_service import reprocess_webhook_event

router = APIRouter(prefix="/webhooks", tags=["admin-webhooks"])


@router.get("", response_model=list[WebhookEventOut])
async def list_webhooks(
    status_filter: WebhookEventStatus | None = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[WebhookEventOut]:
    events = await repo.list_events(db, status=status_filter, limit=limit, offset=offset)
    return [WebhookEventOut.model_validate(e) for e in events]


@router.get("/{event_id}", response_model=WebhookEventDetailOut)
async def get_webhook(
    event_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> WebhookEventDetailOut:
    event = await repo.get_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook introuvable")
    return WebhookEventDetailOut.model_validate(event)


@router.post("/{event_id}/reprocess", response_model=WebhookEventDetailOut)
async def reprocess_webhook(
    event_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> WebhookEventDetailOut:
    event = await repo.get_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Webhook introuvable")

    event = await reprocess_webhook_event(db, event)

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="webhook.reprocess",
        resource_type="webhook_event",
        resource_id=str(event.id),
        after={"status": event.status.value},
        ip_address=request.client.host if request.client else None,
    )
    return WebhookEventDetailOut.model_validate(event)
