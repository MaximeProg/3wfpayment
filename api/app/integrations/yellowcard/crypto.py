"""Appels Yellow Card pour les Crypto Sends (ex-"Settlements") : paiement depuis le
solde du partenaire vers une adresse crypto externe."""

from typing import Any

from app.integrations.yellowcard.client import YellowCardClient


async def submit_crypto_send(client: YellowCardClient, body: dict[str, Any]) -> dict[str, Any]:
    return await client.post("/send/crypto", body=body)


async def lookup_crypto_send_by_sequence_id(client: YellowCardClient, sequence_id: str) -> dict[str, Any]:
    return await client.get(f"/send/crypto/sequence-id/{sequence_id}")


async def list_crypto_sends(client: YellowCardClient, *, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    response = await client.get("/send/crypto", params=params)
    return response.get("settlements", []) if isinstance(response, dict) else response
