from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, verify_api_key_secret
from app.models.project import ApiKey
from app.repositories import api_key_repository


class InvalidApiKeyError(Exception):
    pass


def _parse_api_key(full_key: str) -> tuple[str, str]:
    # Format: "pp_<prefix>_<secret>"
    parts = full_key.split("_", 2)
    if len(parts) != 3 or parts[0] != "pp":
        raise InvalidApiKeyError("Format de cle API invalide")
    return parts[1], parts[2]


async def authenticate_api_key(db: AsyncSession, full_key: str) -> ApiKey:
    prefix, secret = _parse_api_key(full_key)

    candidates = await api_key_repository.list_by_prefix(db, prefix)
    for api_key in candidates:
        if verify_api_key_secret(secret, api_key.key_hash):
            await api_key_repository.touch_last_used(db, api_key)
            return api_key

    raise InvalidApiKeyError("Cle API invalide ou revoquee")


async def issue_access_token(db: AsyncSession, full_key: str) -> str:
    api_key = await authenticate_api_key(db, full_key)
    return create_access_token(subject=str(api_key.project_id), scopes=api_key.scopes)
