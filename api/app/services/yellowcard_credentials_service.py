from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decrypt_secret, encrypt_secret
from app.integrations.yellowcard.client import YellowCardClient
from app.integrations.yellowcard.webhook_signature import verify_webhook_signature
from app.models.enums import Environment
from app.models.yellowcard import YellowCardCredential


async def upsert_credentials(
    db: AsyncSession, *, environment: Environment, api_key: str, api_secret: str, base_url: str
) -> YellowCardCredential:
    result = await db.execute(
        select(YellowCardCredential).where(YellowCardCredential.environment == environment)
    )
    credential = result.scalar_one_or_none()

    if credential is None:
        credential = YellowCardCredential(environment=environment)
        db.add(credential)

    credential.api_key_encrypted = encrypt_secret(api_key)
    credential.api_secret_encrypted = encrypt_secret(api_secret)
    credential.base_url = base_url
    credential.is_active = True

    await db.commit()
    await db.refresh(credential)
    return credential


async def get_active_credential(db: AsyncSession, *, environment: Environment) -> YellowCardCredential | None:
    result = await db.execute(
        select(YellowCardCredential).where(
            YellowCardCredential.environment == environment,
            YellowCardCredential.is_active.is_(True),
        )
    )
    return result.scalar_one_or_none()


async def build_client(db: AsyncSession, *, environment: Environment) -> YellowCardClient:
    credential = await get_active_credential(db, environment=environment)
    if credential is None:
        raise LookupError(f"Aucun credential Yellow Card actif pour l'environnement '{environment.value}'")

    return YellowCardClient(
        api_key=decrypt_secret(credential.api_key_encrypted),
        api_secret=decrypt_secret(credential.api_secret_encrypted),
        base_url=credential.base_url,
    )


async def verify_webhook_and_resolve_environment(
    db: AsyncSession, *, raw_body: bytes, signature_header: str | None, api_key_hint: str | None
) -> Environment | None:
    """Retrouve quel credential (sandbox/production) correspond au webhook recu et
    verifie sa signature X-YC-Signature. Retourne l'environnement si la signature
    est valide, None sinon (pas de credential correspondant ou signature invalide)."""
    if not signature_header:
        return None

    result = await db.execute(select(YellowCardCredential).where(YellowCardCredential.is_active.is_(True)))
    credentials = result.scalars().all()

    for credential in credentials:
        api_key = decrypt_secret(credential.api_key_encrypted)
        if api_key_hint and api_key != api_key_hint:
            continue

        secret = decrypt_secret(credential.api_secret_encrypted)
        if verify_webhook_signature(secret, raw_body, signature_header):
            return credential.environment

    return None
