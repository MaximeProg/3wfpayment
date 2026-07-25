import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import CurrentProject, get_current_project
from app.db.session import get_db
from app.repositories import reference_data_repository as repo
from app.schemas.reference_data import ChannelOut, CountryOut, CurrencyOut, NetworkOut

router = APIRouter(tags=["reference-data"])


@router.get("/countries", response_model=list[CountryOut])
async def list_countries(
    db: AsyncSession = Depends(get_db),
    _current: CurrentProject = Depends(get_current_project),
) -> list[CountryOut]:
    countries = await repo.list_countries(db)
    return [CountryOut.model_validate(c) for c in countries]


@router.get("/networks", response_model=list[NetworkOut])
async def list_networks(
    db: AsyncSession = Depends(get_db),
    _current: CurrentProject = Depends(get_current_project),
) -> list[NetworkOut]:
    networks = await repo.list_networks(db)
    return [NetworkOut.model_validate(n) for n in networks]


@router.get("/currencies", response_model=list[CurrencyOut])
async def list_currencies(
    db: AsyncSession = Depends(get_db),
    _current: CurrentProject = Depends(get_current_project),
) -> list[CurrencyOut]:
    currencies = await repo.list_currencies(db)
    return [CurrencyOut.model_validate(c) for c in currencies]


@router.get("/channels", response_model=list[ChannelOut])
async def list_channels(
    country_id: uuid.UUID | None = Query(None),
    channel_type: str | None = Query(None, description="bank | momo"),
    ramp_type: str | None = Query(None, description="deposit | withdraw"),
    db: AsyncSession = Depends(get_db),
    _current: CurrentProject = Depends(get_current_project),
) -> list[ChannelOut]:
    channels = await repo.list_channels(
        db, country_id=country_id, channel_type=channel_type, ramp_type=ramp_type
    )
    return [ChannelOut.model_validate(c) for c in channels]
