from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.integrations.yellowcard.client import YellowCardAPIError
from app.models.admin import AdminUser
from app.models.enums import AdminRole, ErrorSource
from app.models.enums import Environment as YCEnvironment
from app.repositories import error_repository
from app.schemas.admin import ErrorLogOut, MonitoringHealthOut
from app.services.yellowcard_credentials_service import build_client

router = APIRouter(prefix="/monitoring", tags=["admin-monitoring"])


async def _check_yellowcard(db: AsyncSession, environment: YCEnvironment) -> str:
    try:
        client = await build_client(db, environment=environment)
    except LookupError:
        return "not_configured"

    try:
        await client.get("/account", timeout=5.0)
        return "ok"
    except YellowCardAPIError:
        return "error"
    except Exception:  # noqa: BLE001
        return "unreachable"


@router.get("/health", response_model=MonitoringHealthOut)
async def health(
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> MonitoringHealthOut:
    try:
        await db.execute(text("SELECT 1"))
        database = "ok"
    except Exception:  # noqa: BLE001
        database = "error"

    sandbox = await _check_yellowcard(db, YCEnvironment.sandbox)
    production = await _check_yellowcard(db, YCEnvironment.production)

    return MonitoringHealthOut(database=database, yellowcard_sandbox=sandbox, yellowcard_production=production)


@router.get("/errors", response_model=list[ErrorLogOut])
async def list_errors(
    source: ErrorSource | None = Query(None),
    resolved: bool | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[ErrorLogOut]:
    errors = await error_repository.list_all(db, source=source, resolved=resolved, limit=limit, offset=offset)
    return [ErrorLogOut.model_validate(e) for e in errors]
