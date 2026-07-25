from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole
from app.repositories import audit_repository
from app.schemas.admin import AuditLogOut

router = APIRouter(prefix="/audit-logs", tags=["admin-audit"])


@router.get("", response_model=list[AuditLogOut])
async def list_audit_logs(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.admin)),
) -> list[AuditLogOut]:
    logs = await audit_repository.list_all(db, limit=limit, offset=offset)
    return [AuditLogOut.model_validate(log) for log in logs]
