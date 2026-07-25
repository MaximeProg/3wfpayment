import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ApiKeyStatus
from app.models.project import ApiKey


async def list_by_prefix(db: AsyncSession, key_prefix: str) -> list[ApiKey]:
    """Plusieurs projets ne partagent jamais le meme prefixe en pratique (genere
    aleatoirement), mais on retourne une liste pour rester robuste a une collision."""
    result = await db.execute(
        select(ApiKey).where(ApiKey.key_prefix == key_prefix, ApiKey.status == ApiKeyStatus.active)
    )
    return list(result.scalars().all())


async def create(
    db: AsyncSession,
    *,
    project_id: uuid.UUID,
    key_prefix: str,
    key_hash: str,
    scopes: list[str],
    rotated_from_id: uuid.UUID | None = None,
) -> ApiKey:
    api_key = ApiKey(
        project_id=project_id,
        key_prefix=key_prefix,
        key_hash=key_hash,
        scopes=scopes,
        rotated_from_id=rotated_from_id,
    )
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    return api_key


async def touch_last_used(db: AsyncSession, api_key: ApiKey) -> None:
    api_key.last_used_at = datetime.now(timezone.utc)
    await db.commit()


async def get_by_id(db: AsyncSession, api_key_id: uuid.UUID) -> ApiKey | None:
    return await db.get(ApiKey, api_key_id)


async def list_by_project(db: AsyncSession, project_id: uuid.UUID) -> list[ApiKey]:
    result = await db.execute(
        select(ApiKey).where(ApiKey.project_id == project_id).order_by(ApiKey.created_at.desc())
    )
    return list(result.scalars().all())


async def revoke(db: AsyncSession, api_key: ApiKey) -> ApiKey:
    api_key.status = ApiKeyStatus.revoked
    await db.commit()
    await db.refresh(api_key)
    return api_key
