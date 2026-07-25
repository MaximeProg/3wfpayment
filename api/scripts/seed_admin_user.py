"""Cree le premier administrateur (super_admin) de la plateforme.

Usage: python scripts/seed_admin_user.py <email> <password>
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.security import hash_password  # noqa: E402
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.models.enums import AdminRole  # noqa: E402
from app.repositories import admin_repository  # noqa: E402


async def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python scripts/seed_admin_user.py <email> <password>")
    email, password = sys.argv[1], sys.argv[2]

    if len(password) < 8:
        raise SystemExit("Le mot de passe doit faire au moins 8 caracteres")

    async with AsyncSessionLocal() as db:
        existing = await admin_repository.get_by_email(db, email)
        if existing is not None:
            print(f"Un admin existe deja pour {email} (id={existing.id})")
            return

        admin = await admin_repository.create(
            db, email=email, password_hash=hash_password(password), role=AdminRole.super_admin
        )
        print(f"Admin super_admin cree : {admin.email} (id={admin.id})")


if __name__ == "__main__":
    asyncio.run(main())
