"""Appels Yellow Card pour les depots (Receives) et retraits (Sends).

Terminologie Yellow Card <-> Payment Platform :
- "Receive" (POST /receive) = Yellow Card RECOIT de l'argent d'un payeur  = un DEPOT
  du point de vue de l'utilisateur final (il alimente son wallet).
- "Send" (POST /send)       = Yellow Card ENVOIE de l'argent a un beneficiaire = un
  RETRAIT du point de vue de l'utilisateur final (il retire de son wallet).
"""

from typing import Any

from app.integrations.yellowcard.client import YellowCardClient


async def submit_receive(client: YellowCardClient, body: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/receive", body=body)


async def lookup_receive(client: YellowCardClient, yellowcard_id: str) -> dict[str, Any]:
    return await client.get(f"/receive/{yellowcard_id}")


async def submit_send(client: YellowCardClient, body: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/send", body=body)


async def lookup_send(client: YellowCardClient, yellowcard_id: str) -> dict[str, Any]:
    return await client.get(f"/send/{yellowcard_id}")
