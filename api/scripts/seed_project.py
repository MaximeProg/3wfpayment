"""Cree un premier projet de test (sandbox) avec une cle API, pour valider la
chaine d'authentification /v1/auth/token de bout en bout.

Usage: python scripts/seed_project.py <slug> <name>
Exemple: python scripts/seed_project.py test-client "Test Client"
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import AsyncSessionLocal  # noqa: E402
from app.models.enums import Environment  # noqa: E402
from app.repositories import project_repository  # noqa: E402
from app.services.project_service import create_project, issue_api_key  # noqa: E402


async def main() -> None:
    slug = sys.argv[1] if len(sys.argv) > 1 else "test-client"
    name = sys.argv[2] if len(sys.argv) > 2 else "Test Client"

    async with AsyncSessionLocal() as db:
        project = await project_repository.get_by_slug(db, slug)
        if project is None:
            project = await create_project(db, name=name, slug=slug, environment=Environment.sandbox)
            print(f"Projet cree : {project.id} ({project.slug})")
        else:
            print(f"Projet existant reutilise : {project.id} ({project.slug})")

        api_key, full_key = await issue_api_key(db, project=project)
        print(f"Cle API (prefix={api_key.key_prefix}) - a conserver, non recuperable ensuite :")
        print(full_key)


if __name__ == "__main__":
    asyncio.run(main())
