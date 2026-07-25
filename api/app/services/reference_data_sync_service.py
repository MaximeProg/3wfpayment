"""Synchronise les referentiels locaux (countries/networks/currencies) depuis
Yellow Card. Yellow Card n'expose pas d'endpoint /countries dedie : la liste des
pays est deduite des codes ISO 3166-2 rencontres dans /channels et /networks.
"""

import json
import logging
from datetime import datetime, timezone

import pycountry
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.yellowcard.client import YellowCardClient
from app.integrations.yellowcard.reference_data import get_channels, get_networks, get_rates
from app.models.reference_data import Channel, Country, Currency, Network
from app.repositories import reference_data_repository as repo

logger = logging.getLogger("app.reference_data_sync")


def _country_name(iso_code: str) -> str:
    country = pycountry.countries.get(alpha_2=iso_code)
    return country.name if country else iso_code


def _currency_name(code: str) -> str:
    currency = pycountry.currencies.get(alpha_3=code)
    return currency.name if currency else code


async def _get_or_create_country(db: AsyncSession, iso_code: str, now: datetime) -> Country | None:
    """Retourne None si iso_code n'est pas un vrai code ISO 3166-1 alpha-2 (ex. le
    sentinel "ALL" observe en sandbox sur certains channels/networks "toutes zones"),
    sauf si le pays existe deja en base (deja valide precedemment)."""
    country = await repo.get_country_by_iso(db, iso_code)
    if country is not None:
        country.synced_at = now
        country.is_active = True
        return country

    if pycountry.countries.get(alpha_2=iso_code) is None:
        logger.debug("Code pays ignore (non ISO 3166-1) : %r", iso_code)
        return None

    country = Country(
        iso_code=iso_code,
        name=_country_name(iso_code),
        is_active=True,
        raw_data={"source": "derived_from_channels_networks"},
        synced_at=now,
    )
    db.add(country)
    await db.flush()
    return country


async def sync_channels(db: AsyncSession, client: YellowCardClient) -> int:
    """Synchronise les channels (rails de paiement) et, au passage, les pays qui y
    apparaissent. channelId (pas channelType) est requis pour soumettre un depot/
    retrait de facon fiable (constate en sandbox - cf. docstring du modele Channel)."""
    channels = await get_channels(client)
    now = datetime.now(timezone.utc)

    count = 0
    for item in channels:
        iso_code = item.get("country")
        if not iso_code:
            continue
        country = await _get_or_create_country(db, iso_code, now)
        if country is None:
            continue

        channel = await repo.get_channel_by_yellowcard_id(db, item["id"])
        if channel is None:
            channel = Channel(yellowcard_id=item["id"], country_id=country.id)
            db.add(channel)

        channel.country_id = country.id
        channel.currency_code = item.get("currency", "")
        channel.channel_type = item.get("channelType", "unknown")
        channel.ramp_type = item.get("rampType", "unknown")
        channel.status = item.get("status", "unknown")
        channel.api_status = item.get("apiStatus", "unknown")
        channel.min_amount = item.get("min")
        channel.max_amount = item.get("max")
        channel.raw_data = item
        channel.synced_at = now
        count += 1

    await db.commit()
    logger.info("Sync channels : %d channels synchronises", count)
    return count


async def sync_networks(db: AsyncSession, client: YellowCardClient) -> int:
    networks = await get_networks(client)
    now = datetime.now(timezone.utc)

    count = 0
    for item in networks:
        iso_code = item.get("country")
        if not iso_code:
            continue
        country = await _get_or_create_country(db, iso_code, now)
        if country is None:
            continue

        network = await repo.get_network_by_yellowcard_id(db, item["id"])
        if network is None:
            network = Network(yellowcard_id=item["id"], country_id=country.id)
            db.add(network)

        code_value = item.get("code", "")
        if not isinstance(code_value, str):
            # Vu en sandbox : certains reseaux renvoient "code" comme un objet
            # (ex. mapping agence -> code) plutot qu'une chaine simple.
            code_value = json.dumps(code_value)

        network.country_id = country.id
        network.name = item.get("name", "")
        network.code = code_value
        network.channel_type = item.get("accountNumberType", "unknown")
        network.status = item.get("status", "unknown")
        network.raw_data = item
        network.synced_at = now
        count += 1

    await db.commit()
    logger.info("Sync networks : %d networks synchronises", count)
    return count


async def sync_currencies(db: AsyncSession, client: YellowCardClient) -> int:
    payload = await get_rates(client)
    rates = payload.get("rates", []) if isinstance(payload, dict) else payload
    now = datetime.now(timezone.utc)

    count = 0
    for rate in rates:
        code = rate.get("code")
        if not code:
            continue

        country: Country | None = None
        locale = rate.get("locale")
        if locale:
            country = await _get_or_create_country(db, locale, now)

        currency = await repo.get_currency_by_code(db, code)
        if currency is None:
            currency = Currency(code=code, name=_currency_name(code))
            db.add(currency)
            # Le meme code devise (ex. "USD") peut apparaitre plusieurs fois dans
            # /rates pour differents pays : flush immediat pour que la recherche
            # suivante le retrouve (autoflush est desactive sur la session).
            await db.flush()

        currency.name = _currency_name(code)
        currency.country_id = country.id if country else currency.country_id
        currency.is_active = True
        count += 1

    await db.commit()
    logger.info("Sync currencies : %d devises synchronisees", count)
    return count


async def sync_all(db: AsyncSession, client: YellowCardClient) -> dict[str, int]:
    channels = await sync_channels(db, client)
    networks = await sync_networks(db, client)
    currencies = await sync_currencies(db, client)
    return {
        "channels": channels,
        "networks": networks,
        "currencies": currencies,
    }
