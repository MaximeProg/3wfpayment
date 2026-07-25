from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole, AuditActorType
from app.repositories import audit_repository, settings_repository
from app.schemas.admin import SystemSettingOut, SystemSettingUpdateRequest

router = APIRouter(prefix="/settings", tags=["admin-settings"])


@router.get("", response_model=list[SystemSettingOut])
async def list_settings(
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[SystemSettingOut]:
    settings = await settings_repository.list_all(db)
    return [SystemSettingOut.model_validate(s) for s in settings]


@router.patch("/{key}", response_model=SystemSettingOut)
async def update_setting(
    key: str,
    payload: SystemSettingUpdateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    admin: AdminUser = Depends(require_admin_role(AdminRole.super_admin)),
) -> SystemSettingOut:
    before = await settings_repository.get_by_key(db, key)
    before_value = before.value if before else None

    setting = await settings_repository.upsert(
        db, key=key, value=payload.value, description=payload.description, updated_by=str(admin.id)
    )

    await audit_repository.create(
        db,
        actor_type=AuditActorType.admin,
        actor_id=str(admin.id),
        action="setting.update",
        resource_type="system_setting",
        resource_id=key,
        before={"value": before_value},
        after={"value": setting.value},
        ip_address=request.client.host if request.client else None,
    )
    return SystemSettingOut.model_validate(setting)
