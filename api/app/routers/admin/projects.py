import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole, ApiKeyStatus, AuditActorType, Environment, ProjectStatus
from app.repositories import api_key_repository, audit_repository, project_repository
from app.schemas.admin import (
    ApiKeyCreatedOut,
    ApiKeyCreateRequest,
    ApiKeyOut,
    ProjectCreateRequest,
    ProjectOut,
    ProjectUpdateRequest,
)
from app.services.project_service import create_project, issue_api_key, rotate_api_key

router = APIRouter(prefix="/projects", tags=["admin-projects"])


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("", response_model=list[ProjectOut])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[ProjectOut]:
    projects = await project_repository.list_all(db)
    return [ProjectOut.model_validate(p) for p in projects]


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_project_endpoint(
    payload: ProjectCreateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> ProjectOut:
    try:
        environment = Environment(payload.environment)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="environment invalide") from exc

    try:
        project = await create_project(
            db,
            name=payload.name,
            slug=payload.slug,
            description=payload.description,
            environment=environment,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="project.create",
        resource_type="project",
        resource_id=str(project.id),
        after={"name": project.name, "slug": project.slug, "environment": project.environment.value},
        ip_address=_client_ip(request),
    )
    return ProjectOut.model_validate(project)


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> ProjectOut:
    project = await project_repository.get_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projet introuvable")
    return ProjectOut.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectOut)
async def update_project(
    project_id: uuid.UUID,
    payload: ProjectUpdateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> ProjectOut:
    project = await project_repository.get_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projet introuvable")

    before = {"name": project.name, "description": project.description, "status": project.status.value}

    new_status = None
    if payload.status is not None:
        try:
            new_status = ProjectStatus(payload.status)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="status invalide") from exc

    project = await project_repository.update(
        db, project, name=payload.name, description=payload.description, status=new_status
    )

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="project.update",
        resource_type="project",
        resource_id=str(project.id),
        before=before,
        after={"name": project.name, "description": project.description, "status": project.status.value},
        ip_address=_client_ip(request),
    )
    return ProjectOut.model_validate(project)


@router.get("/{project_id}/api-keys", response_model=list[ApiKeyOut])
async def list_project_api_keys(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[ApiKeyOut]:
    project = await project_repository.get_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projet introuvable")
    keys = await api_key_repository.list_by_project(db, project_id)
    return [ApiKeyOut.model_validate(k) for k in keys]


@router.post("/{project_id}/api-keys", response_model=ApiKeyCreatedOut, status_code=status.HTTP_201_CREATED)
async def create_project_api_key(
    project_id: uuid.UUID,
    payload: ApiKeyCreateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> ApiKeyCreatedOut:
    project = await project_repository.get_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projet introuvable")

    api_key, full_key = await issue_api_key(db, project=project, scopes=payload.scopes)

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="api_key.create",
        resource_type="api_key",
        resource_id=str(api_key.id),
        after={"project_id": str(project.id), "key_prefix": api_key.key_prefix, "scopes": api_key.scopes},
        ip_address=_client_ip(request),
    )
    return ApiKeyCreatedOut(**ApiKeyOut.model_validate(api_key).model_dump(), full_key=full_key)


@router.post("/api-keys/{api_key_id}/rotate", response_model=ApiKeyCreatedOut)
async def rotate_project_api_key(
    api_key_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> ApiKeyCreatedOut:
    old_key = await api_key_repository.get_by_id(db, api_key_id)
    if old_key is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cle API introuvable")
    project = await project_repository.get_by_id(db, old_key.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Projet introuvable")

    new_key, full_key = await rotate_api_key(db, project=project, old_key=old_key)

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="api_key.rotate",
        resource_type="api_key",
        resource_id=str(new_key.id),
        before={"rotated_from": str(old_key.id)},
        after={"project_id": str(project.id), "key_prefix": new_key.key_prefix},
        ip_address=_client_ip(request),
    )
    return ApiKeyCreatedOut(**ApiKeyOut.model_validate(new_key).model_dump(), full_key=full_key)


@router.post("/api-keys/{api_key_id}/revoke", response_model=ApiKeyOut)
async def revoke_project_api_key(
    api_key_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> ApiKeyOut:
    api_key = await api_key_repository.get_by_id(db, api_key_id)
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cle API introuvable")
    if api_key.status == ApiKeyStatus.revoked:
        return ApiKeyOut.model_validate(api_key)

    api_key = await api_key_repository.revoke(db, api_key)

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="api_key.revoke",
        resource_type="api_key",
        resource_id=str(api_key.id),
        after={"status": api_key.status.value},
        ip_address=_client_ip(request),
    )
    return ApiKeyOut.model_validate(api_key)
