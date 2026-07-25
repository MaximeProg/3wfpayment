import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import AdminUser
from app.models.enums import AdminRole, NotificationCategory, NotificationSeverity
from app.models.notification import Notification, NotificationRead

_ROLE_RANK = {AdminRole.viewer: 0, AdminRole.admin: 1, AdminRole.super_admin: 2}


def _visible_roles(admin_role: AdminRole) -> list[AdminRole]:
    rank = _ROLE_RANK[admin_role]
    return [role for role, role_rank in _ROLE_RANK.items() if role_rank <= rank]


async def create(
    db: AsyncSession,
    *,
    category: NotificationCategory,
    severity: NotificationSeverity,
    title: str,
    message: str,
    audience_min_role: AdminRole,
    related_type: str | None = None,
    related_id: str | None = None,
) -> Notification:
    notification = Notification(
        category=category,
        severity=severity,
        title=title,
        message=message,
        audience_min_role=audience_min_role,
        related_type=related_type,
        related_id=related_id,
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def list_for_admin(
    db: AsyncSession,
    admin: AdminUser,
    *,
    unread_only: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> list[tuple[Notification, bool]]:
    read_exists = (
        select(NotificationRead.notification_id)
        .where(NotificationRead.notification_id == Notification.id, NotificationRead.admin_id == admin.id)
        .exists()
    )
    query = (
        select(Notification, read_exists.label("is_read"))
        .where(Notification.audience_min_role.in_(_visible_roles(admin.role)))
        .order_by(Notification.created_at.desc())
    )
    if unread_only:
        query = query.where(~read_exists)
    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    return [(row[0], bool(row[1])) for row in result.all()]


async def unread_count_for_admin(db: AsyncSession, admin: AdminUser) -> int:
    read_exists = (
        select(NotificationRead.notification_id)
        .where(NotificationRead.notification_id == Notification.id, NotificationRead.admin_id == admin.id)
        .exists()
    )
    query = (
        select(func.count())
        .select_from(Notification)
        .where(Notification.audience_min_role.in_(_visible_roles(admin.role)), ~read_exists)
    )
    result = await db.execute(query)
    return int(result.scalar_one())


async def mark_read(db: AsyncSession, *, notification_id: uuid.UUID, admin_id: uuid.UUID) -> None:
    existing = await db.get(NotificationRead, {"notification_id": notification_id, "admin_id": admin_id})
    if existing is not None:
        return
    db.add(NotificationRead(notification_id=notification_id, admin_id=admin_id))
    await db.commit()


async def mark_all_read(db: AsyncSession, admin: AdminUser) -> None:
    read_exists = (
        select(NotificationRead.notification_id)
        .where(NotificationRead.notification_id == Notification.id, NotificationRead.admin_id == admin.id)
        .exists()
    )
    query = select(Notification.id).where(
        Notification.audience_min_role.in_(_visible_roles(admin.role)), ~read_exists
    )
    result = await db.execute(query)
    unread_ids = result.scalars().all()
    for notification_id in unread_ids:
        db.add(NotificationRead(notification_id=notification_id, admin_id=admin.id))
    if unread_ids:
        await db.commit()
