"""Verification manuelle : appelle GET /business/channels sur le sandbox Yellow Card
en utilisant les credentials stockes en base (chiffres), pour valider que la
signature HMAC est correcte de bout en bout.

Usage: python scripts/check_yellowcard_auth.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import AsyncSessionLocal  # noqa: E402
from app.integrations.yellowcard.reference_data import get_channels  # noqa: E402
from app.models.enums import Environment  # noqa: E402
from app.services.yellowcard_credentials_service import build_client  # noqa: E402


async def main() -> None:
    async with AsyncSessionLocal() as db:
        client = await build_client(db, environment=Environment.sandbox)

    channels = await get_channels(client)
    print(f"OK - reponse recue depuis le sandbox Yellow Card (type={type(channels).__name__})")
    print(channels)


if __name__ == "__main__":
    asyncio.run(main())
