from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reference_data import Channel, Country, Currency, Network


async def get_country_by_iso(db: AsyncSession, iso_code: str) -> Country | None:
    result = await db.execute(select(Country).where(Country.iso_code == iso_code))
    return result.scalar_one_or_none()


async def list_countries(db: AsyncSession, *, active_only: bool = True) -> list[Country]:
    query = select(Country).order_by(Country.name)
    if active_only:
        query = query.where(Country.is_active.is_(True))
    result = await db.execute(query)
    return list(result.scalars().all())


async def list_networks(
    db: AsyncSession, *, country_id=None, active_only: bool = True
) -> list[Network]:
    query = select(Network).order_by(Network.name)
    if active_only:
        query = query.where(Network.status == "active")
    if country_id is not None:
        query = query.where(Network.country_id == country_id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def list_currencies(db: AsyncSession, *, active_only: bool = True) -> list[Currency]:
    query = select(Currency).order_by(Currency.code)
    if active_only:
        query = query.where(Currency.is_active.is_(True))
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_network_by_yellowcard_id(db: AsyncSession, yellowcard_id: str) -> Network | None:
    result = await db.execute(select(Network).where(Network.yellowcard_id == yellowcard_id))
    return result.scalar_one_or_none()


async def get_network_by_id(db: AsyncSession, network_id) -> Network | None:
    return await db.get(Network, network_id)


async def get_currency_by_code(db: AsyncSession, code: str) -> Currency | None:
    result = await db.execute(select(Currency).where(Currency.code == code))
    return result.scalar_one_or_none()


async def get_channel_by_yellowcard_id(db: AsyncSession, yellowcard_id: str) -> Channel | None:
    result = await db.execute(select(Channel).where(Channel.yellowcard_id == yellowcard_id))
    return result.scalar_one_or_none()


async def get_channel_by_id(db: AsyncSession, channel_id) -> Channel | None:
    return await db.get(Channel, channel_id)


async def list_channels(
    db: AsyncSession,
    *,
    country_id=None,
    channel_type: str | None = None,
    ramp_type: str | None = None,
    active_only: bool = True,
) -> list[Channel]:
    query = select(Channel).order_by(Channel.currency_code)
    if active_only:
        query = query.where(Channel.status == "active", Channel.api_status == "active")
    if country_id is not None:
        query = query.where(Channel.country_id == country_id)
    if channel_type is not None:
        query = query.where(Channel.channel_type == channel_type)
    if ramp_type is not None:
        query = query.where(Channel.ramp_type == ramp_type)
    result = await db.execute(query)
    return list(result.scalars().all())
