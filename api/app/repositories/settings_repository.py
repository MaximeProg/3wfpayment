from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.settings import SystemSetting


async def list_all(db: AsyncSession) -> list[SystemSetting]:
    result = await db.execute(select(SystemSetting).order_by(SystemSetting.key))
    return list(result.scalars().all())


async def get_by_key(db: AsyncSession, key: str) -> SystemSetting | None:
    return await db.get(SystemSetting, key)


async def upsert(
    db: AsyncSession, *, key: str, value, description: str | None, updated_by: str
) -> SystemSetting:
    setting = await db.get(SystemSetting, key)
    if setting is None:
        setting = SystemSetting(key=key)
        db.add(setting)

    setting.value = value
    if description is not None:
        setting.description = description
    setting.updated_by = updated_by

    await db.commit()
    await db.refresh(setting)
    return setting
