import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole, AuditActorType
from app.repositories import audit_repository
from app.schemas.admin import (
    AdminActiveUpdateRequest,
    AdminInviteRequest,
    AdminManagedOut,
    AdminRoleUpdateRequest,
)
from app.services.admin_management_service import (
    CannotActOnSelfError,
    invite_admin,
    list_admins,
    set_admin_active,
    update_admin_role,
)

router = APIRouter(prefix="/admins", tags=["admin-management"])


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("", response_model=list[AdminManagedOut])
async def list_admins_endpoint(
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> list[AdminManagedOut]:
    admins = await list_admins(db)
    return [AdminManagedOut.model_validate(a) for a in admins]


@router.post("", response_model=AdminManagedOut, status_code=status.HTTP_201_CREATED)
async def invite_admin_endpoint(
    payload: AdminInviteRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.super_admin)),
) -> AdminManagedOut:
    try:
        role = AdminRole(payload.role)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="role invalide") from exc

    new_admin = await invite_admin(db, inviter=admin, email=payload.email, role=role)

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="admin.invite",
        resource_type="admin",
        resource_id=str(new_admin.id),
        after={"email": new_admin.email, "role": new_admin.role.value},
        ip_address=_client_ip(request),
    )
    return AdminManagedOut.model_validate(new_admin)


@router.patch("/{admin_id}/role", response_model=AdminManagedOut)
async def update_admin_role_endpoint(
    admin_id: uuid.UUID,
    payload: AdminRoleUpdateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.super_admin)),
) -> AdminManagedOut:
    try:
        role = AdminRole(payload.role)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="role invalide") from exc

    try:
        target = await update_admin_role(db, actor=admin, target_id=admin_id, role=role)
    except CannotActOnSelfError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="admin.update_role",
        resource_type="admin",
        resource_id=str(target.id),
        after={"role": target.role.value},
        ip_address=_client_ip(request),
    )
    return AdminManagedOut.model_validate(target)


@router.patch("/{admin_id}/active", response_model=AdminManagedOut)
async def update_admin_active_endpoint(
    admin_id: uuid.UUID,
    payload: AdminActiveUpdateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.super_admin)),
) -> AdminManagedOut:
    try:
        target = await set_admin_active(db, actor=admin, target_id=admin_id, is_active=payload.is_active)
    except CannotActOnSelfError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="admin.set_active",
        resource_type="admin",
        resource_id=str(target.id),
        after={"is_active": target.is_active},
        ip_address=_client_ip(request),
    )
    return AdminManagedOut.model_validate(target)
