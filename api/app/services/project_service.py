from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_api_key
from app.models.enums import Environment
from app.models.project import ApiKey, Project
from app.repositories import api_key_repository, project_repository

DEFAULT_SCOPES = ["deposits:write", "withdrawals:write", "transactions:read"]


async def create_project(
    db: AsyncSession, *, name: str, slug: str, description: str | None = None, environment: Environment
) -> Project:
    existing = await project_repository.get_by_slug(db, slug)
    if existing is not None:
        raise ValueError(f"Un projet avec le slug '{slug}' existe deja")

    return await project_repository.create(
        db, name=name, slug=slug, description=description, environment=environment
    )


async def issue_api_key(
    db: AsyncSession, *, project: Project, scopes: list[str] | None = None, rotated_from_id=None
) -> tuple[ApiKey, str]:
    """Retourne (enregistrement ApiKey, cle complete en clair). La cle complete
    n'est jamais recuperable apres cet appel : seul son hash est conserve."""
    full_key, prefix, key_hash = generate_api_key()
    api_key = await api_key_repository.create(
        db,
        project_id=project.id,
        key_prefix=prefix,
        key_hash=key_hash,
        scopes=scopes or DEFAULT_SCOPES,
        rotated_from_id=rotated_from_id,
    )
    return api_key, full_key


async def rotate_api_key(db: AsyncSession, *, project: Project, old_key: ApiKey) -> tuple[ApiKey, str]:
    """Emet une nouvelle cle (memes scopes) et revoque l'ancienne. La cle complete
    de la nouvelle n'est affichee qu'une fois, comme a la creation."""
    new_key, full_key = await issue_api_key(
        db, project=project, scopes=old_key.scopes, rotated_from_id=old_key.id
    )
    await api_key_repository.revoke(db, old_key)
    return new_key, full_key
