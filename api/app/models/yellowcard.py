from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPKMixin
from app.models.enums import Environment


class YellowCardCredential(UUIDPKMixin, TimestampMixin, Base):
    """Identifiants Yellow Card (par environnement). L'authentification Yellow Card
    signe chaque requete individuellement (HMAC-SHA256, schema YcHmacV1) avec la cle
    API et le secret : il n'y a pas de jeton OAuth a obtenir ni a renouveler."""

    __tablename__ = "yellowcard_credentials"

    environment: Mapped[Environment] = mapped_column(
        Enum(Environment, name="environment"), nullable=False, unique=True
    )
    api_key_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    api_secret_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
