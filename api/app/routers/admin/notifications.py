import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole
from app.repositories import notification_repository
from app.schemas.admin import NotificationOut, UnreadCountOut

router = APIRouter(prefix="/notifications", tags=["admin-notifications"])


@router.get("", response_model=list[NotificationOut])
async def list_notifications(
    unread_only: bool = Query(False),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[NotificationOut]:
    rows = await notification_repository.list_for_admin(
        db, admin, unread_only=unread_only, limit=limit, offset=offset
    )
    return [
        NotificationOut(
            id=n.id,
            category=n.category.value,
            severity=n.severity.value,
            title=n.title,
            message=n.message,
            related_type=n.related_type,
            related_id=n.related_id,
            is_read=is_read,
            created_at=n.created_at,
        )
        for n, is_read in rows
    ]


@router.get("/unread-count", response_model=UnreadCountOut)
async def unread_count(
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> UnreadCountOut:
    count = await notification_repository.unread_count_for_admin(db, admin)
    return UnreadCountOut(count=count)


@router.post("/{notification_id}/read")
async def mark_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> dict:
    await notification_repository.mark_read(db, notification_id=notification_id, admin_id=admin.id)
    return {"read": True}


@router.post("/read-all")
async def mark_all_read(
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> dict:
    await notification_repository.mark_all_read(db, admin)
    return {"read": True}
