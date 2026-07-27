"""Configure l'URL de webhook sortant d'un projet (et genere son secret si absent).

A executer une fois l'URL publique du backend consommateur connue. Le secret
n'est affiche qu'a cette occasion : le copier immediatement dans le .env du
projet consommateur (ex. PAYMENT_PLATFORM_WEBHOOK_SECRET pour 3WF).

Usage: python scripts/set_project_webhook.py <slug> <webhook_url>
"""

import asyncio
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.security import decrypt_secret, encrypt_secret  # noqa: E402
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.repositories import project_repository  # noqa: E402


async def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python scripts/set_project_webhook.py <slug> <webhook_url>")
    slug, webhook_url = sys.argv[1], sys.argv[2]

    async with AsyncSessionLocal() as db:
        project = await project_repository.get_by_slug(db, slug)
        if project is None:
            raise SystemExit(f"Aucun projet avec le slug '{slug}'")

        new_secret_encrypted = None
        if not project.webhook_secret_encrypted:
            new_secret_encrypted = encrypt_secret(secrets.token_urlsafe(32))

        project = await project_repository.update(
            db, project, webhook_url=webhook_url, webhook_secret_encrypted=new_secret_encrypted
        )

        secret = decrypt_secret(project.webhook_secret_encrypted)
        print(f"Webhook configure pour '{project.slug}' : {project.webhook_url}")
        print(f"Secret (a copier dans le .env du projet consommateur) : {secret}")


if __name__ == "__main__":
    asyncio.run(main())
