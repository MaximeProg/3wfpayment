import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import Environment, ProjectStatus
from app.models.project import Project


async def get_by_id(db: AsyncSession, project_id: uuid.UUID) -> Project | None:
    return await db.get(Project, project_id)


async def get_by_slug(db: AsyncSession, slug: str) -> Project | None:
    result = await db.execute(select(Project).where(Project.slug == slug))
    return result.scalar_one_or_none()


async def list_all(db: AsyncSession) -> list[Project]:
    result = await db.execute(select(Project).order_by(Project.created_at))
    return list(result.scalars().all())


async def create(
    db: AsyncSession, *, name: str, slug: str, description: str | None, environment: Environment
) -> Project:
    project = Project(
        name=name,
        slug=slug,
        description=description,
        environment=environment,
        status=ProjectStatus.active,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def update(
    db: AsyncSession,
    project: Project,
    *,
    name: str | None = None,
    description: str | None = None,
    status: ProjectStatus | None = None,
) -> Project:
    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    if status is not None:
        project.status = status
    await db.commit()
    await db.refresh(project)
    return project
