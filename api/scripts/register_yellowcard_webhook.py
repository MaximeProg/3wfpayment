"""Enregistre l'URL publique de reception des webhooks aupres de Yellow Card.

A n'utiliser qu'une fois l'API deployee sur une URL publique (ou exposee via un
tunnel type ngrok pour des tests sandbox) : Yellow Card ne peut pas joindre
http://127.0.0.1.

Usage: python scripts/register_yellowcard_webhook.py https://mon-domaine.example/internal/webhooks/yellowcard
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import AsyncSessionLocal  # noqa: E402
from app.integrations.yellowcard.webhooks import create_webhook  # noqa: E402
from app.models.enums import Environment  # noqa: E402
from app.services.yellowcard_credentials_service import build_client  # noqa: E402


async def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/register_yellowcard_webhook.py <url_publique>")
    url = sys.argv[1]

    async with AsyncSessionLocal() as db:
        client = await build_client(db, environment=Environment.sandbox)

    result = await create_webhook(client, url=url)
    print(f"Webhook enregistre : {result}")


if __name__ == "__main__":
    asyncio.run(main())
