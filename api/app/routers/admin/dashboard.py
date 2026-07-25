from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import require_admin_role
from app.db.session import get_db
from app.models.admin import AdminUser
from app.models.enums import AdminRole
from app.models.enums import Environment as YCEnvironment
from app.schemas.admin import DashboardOverviewOut, ProjectActivityOut, YellowCardBalanceOut
from app.services.admin_stats_service import get_activity_by_project, get_overview
from app.services.yellowcard_credentials_service import build_client

router = APIRouter(prefix="/stats", tags=["admin-dashboard"])


@router.get("/overview", response_model=DashboardOverviewOut)
async def stats_overview(
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> DashboardOverviewOut:
    return await get_overview(db)


@router.get("/by-project", response_model=list[ProjectActivityOut])
async def stats_by_project(
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[ProjectActivityOut]:
    return await get_activity_by_project(db)


@router.get("/yellowcard-balance", response_model=list[YellowCardBalanceOut])
async def yellowcard_balance(
    db: AsyncSession = Depends(get_db),
    _admin: AdminUser = Depends(require_admin_role(AdminRole.viewer)),
) -> list[YellowCardBalanceOut]:
    balances: list[YellowCardBalanceOut] = []
    for environment in (YCEnvironment.sandbox, YCEnvironment.production):
        try:
            client = await build_client(db, environment=environment)
        except LookupError:
            continue
        try:
            response = await client.get("/account", timeout=8.0)
        except Exception:  # noqa: BLE001
            continue
        accounts = response.get("accounts", []) if isinstance(response, dict) else []
        balances.append(
            YellowCardBalanceOut(
                environment=environment.value,
                accounts=[
                    {
                        "available": a.get("available", 0),
                        "currency": a.get("currency", ""),
                        "currency_type": a.get("currencyType", ""),
                    }
                    for a in accounts
                ],
            )
        )
    return balances
