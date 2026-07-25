from typing import Any

from app.integrations.yellowcard.client import YellowCardClient


async def create_webhook(
    client: YellowCardClient, *, url: str, state: str | None = None, active: bool = True
) -> dict[str, Any]:
    body: dict[str, Any] = {"url": url, "active": active}
    if state:
        body["state"] = state
    return await client.post("/webhooks", body=body)


async def list_webhooks(client: YellowCardClient) -> list[dict[str, Any]]:
    response = await client.get("/webhooks")
    return response.get("webhooks", []) if isinstance(response, dict) else response


async def delete_webhook(client: YellowCardClient, webhook_id: str) -> Any:
    return await client.delete(f"/webhooks/{webhook_id}")
