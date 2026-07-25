"""Appels Yellow Card pour les referentiels (channels, networks, rates).

Note : la doc publique montre un tableau brut en reponse de GET /channels, mais la
verification en sandbox (24/07/2026) a montre une reponse enveloppee
`{"channels": [...]}`. Le meme schema d'enveloppe (cle = nom de la ressource) est
donc suppose pour /networks, a reconfirmer a la premiere utilisation reelle.
"""

from typing import Any

from app.integrations.yellowcard.client import YellowCardClient


async def get_channels(client: YellowCardClient, *, country: str | None = None) -> list[dict[str, Any]]:
    params = {"country": country} if country else None
    response = await client.get("/channels", params=params)
    return response.get("channels", []) if isinstance(response, dict) else response


async def get_networks(client: YellowCardClient, *, country: str | None = None) -> list[dict[str, Any]]:
    params = {"country": country} if country else None
    response = await client.get("/networks", params=params)
    return response.get("networks", []) if isinstance(response, dict) else response


async def get_rates(client: YellowCardClient, *, currency: str | None = None) -> dict[str, Any]:
    params = {"currency": currency} if currency else None
    return await client.get("/rates", params=params)


async def get_account(client: YellowCardClient) -> dict[str, Any]:
    return await client.get("/account")
