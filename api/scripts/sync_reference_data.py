"""Synchronise les referentiels (pays/networks/devises) depuis le sandbox Yellow Card.

Usage: python scripts/sync_reference_data.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import AsyncSessionLocal  # noqa: E402
from app.models.enums import Environment  # noqa: E402
from app.services.reference_data_sync_service import sync_all  # noqa: E402
from app.services.yellowcard_credentials_service import build_client  # noqa: E402


async def main() -> None:
    async with AsyncSessionLocal() as db:
        client = await build_client(db, environment=Environment.sandbox)
        result = await sync_all(db, client)
        print(f"Synchronisation terminee : {result}")


if __name__ == "__main__":
    asyncio.run(main())
