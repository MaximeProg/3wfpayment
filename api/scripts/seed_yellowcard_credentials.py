"""Seed initial : enregistre en base (chiffres) les credentials Yellow Card Sandbox
lus depuis les variables d'environnement (.env). A relancer si les credentials
sandbox sont regeneres, ou pour ajouter les credentials de production plus tard.

Usage: python scripts/seed_yellowcard_credentials.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings  # noqa: E402
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.models.enums import Environment  # noqa: E402
from app.services.yellowcard_credentials_service import upsert_credentials  # noqa: E402


async def main() -> None:
    settings = get_settings()

    if not settings.yellowcard_api_key or not settings.yellowcard_api_secret:
        raise SystemExit("YELLOWCARD_API_KEY / YELLOWCARD_API_SECRET manquants dans .env")

    async with AsyncSessionLocal() as db:
        credential = await upsert_credentials(
            db,
            environment=Environment.sandbox,
            api_key=settings.yellowcard_api_key,
            api_secret=settings.yellowcard_api_secret,
            base_url=settings.yellowcard_base_url,
        )
        print(f"Credentials Yellow Card ({credential.environment.value}) enregistrees : id={credential.id}")


if __name__ == "__main__":
    asyncio.run(main())
