import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin import AdminUser


async def get_by_id(db: AsyncSession, admin_id: uuid.UUID) -> AdminUser | None:
    return await db.get(AdminUser, admin_id)


async def get_by_email(db: AsyncSession, email: str) -> AdminUser | None:
    result = await db.execute(select(AdminUser).where(AdminUser.email == email.lower()))
    return result.scalar_one_or_none()


async def list_all(db: AsyncSession) -> list[AdminUser]:
    result = await db.execute(select(AdminUser).order_by(AdminUser.created_at))
    return list(result.scalars().all())


async def create(
    db: AsyncSession, *, email: str, password_hash: str, role, invited_by_id: uuid.UUID | None = None
) -> AdminUser:
    admin = AdminUser(email=email.lower(), password_hash=password_hash, role=role, invited_by_id=invited_by_id)
    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return admin


async def touch_last_login(db: AsyncSession, admin: AdminUser) -> None:
    admin.last_login_at = datetime.now(timezone.utc)
    await db.commit()


async def update_role(db: AsyncSession, admin: AdminUser, role) -> AdminUser:
    admin.role = role
    await db.commit()
    await db.refresh(admin)
    return admin


async def set_active(db: AsyncSession, admin: AdminUser, is_active: bool) -> AdminUser:
    admin.is_active = is_active
    await db.commit()
    await db.refresh(admin)
    return admin


async def update_password_hash(db: AsyncSession, admin: AdminUser, password_hash: str) -> AdminUser:
    admin.password_hash = password_hash
    await db.commit()
    await db.refresh(admin)
    return admin
