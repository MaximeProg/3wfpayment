import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet

from app.core.config import get_settings

settings = get_settings()

_password_hasher = PasswordHasher()
_fernet = Fernet(settings.encryption_key.encode())


# --- Mots de passe admin ---


def hash_password(password: str) -> str:
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


# --- Cles API projet ---
# Format expose au client : "pp_<prefix>_<secret>". Seul key_hash (du secret) est stocke en base.


def generate_api_key() -> tuple[str, str, str]:
    """Retourne (cle_complete_a_afficher_une_fois, key_prefix, key_hash)."""
    prefix = secrets.token_hex(4)
    secret = secrets.token_urlsafe(32)
    full_key = f"pp_{prefix}_{secret}"
    key_hash = _password_hasher.hash(secret)
    return full_key, prefix, key_hash


def verify_api_key_secret(secret: str, key_hash: str) -> bool:
    try:
        return _password_hasher.verify(key_hash, secret)
    except VerifyMismatchError:
        return False


# --- JWT (echange API key/secret -> token court pour les projets clients) ---


def create_access_token(*, subject: str, scopes: list[str], extra_claims: dict[str, Any] | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "scopes": scopes,
        "type": "project",
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
        **(extra_claims or {}),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


# --- JWT (session dashboard admin, transportee via cookie httpOnly) ---


def create_admin_session_token(*, admin_id: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": admin_id,
        "role": role,
        "type": "admin",
        "iat": now,
        "exp": now + timedelta(minutes=settings.admin_session_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


# --- Chiffrement at-rest (credentials / tokens Yellow Card) ---


def encrypt_secret(plaintext: str) -> str:
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt_secret(ciphertext: str) -> str:
    return _fernet.decrypt(ciphertext.encode()).decode()
