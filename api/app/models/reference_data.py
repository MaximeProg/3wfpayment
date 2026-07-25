import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDPKMixin


class Country(UUIDPKMixin, Base):
    """Yellow Card n'expose pas d'endpoint /countries dedie : les pays sont deduits
    des codes ISO 3166-2 presents dans les reponses /channels et /networks. iso_code
    est donc la cle naturelle (il n'y a pas d'id Yellow Card au niveau pays)."""

    __tablename__ = "countries"

    iso_code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    raw_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    synced_at: Mapped[datetime] = mapped_column(nullable=False)


class Network(UUIDPKMixin, Base):
    __tablename__ = "networks"

    yellowcard_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # Text (pas String) : certains reseaux renvoient "code" comme un objet serialise
    # (mapping agence -> code) plutot qu'un simple code court.
    code: Mapped[str] = mapped_column(Text, nullable=False)
    channel_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    raw_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    synced_at: Mapped[datetime] = mapped_column(nullable=False)


class Channel(UUIDPKMixin, Base):
    """Un "channel" Yellow Card = un rail de paiement concret (ex: momo deposit au
    Cameroun en XAF). C'est channelId, pas channelType, qui doit etre utilise pour
    soumettre un depot/retrait : l'alternative "channelType" documentee par Yellow
    Card ne trouve pas toujours de canal actif en sandbox (constate le 24/07/2026)."""

    __tablename__ = "channels"

    yellowcard_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    country_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("countries.id", ondelete="CASCADE"), nullable=False, index=True
    )
    currency_code: Mapped[str] = mapped_column(String(8), nullable=False, index=True)
    channel_type: Mapped[str] = mapped_column(String(32), nullable=False)
    ramp_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    api_status: Mapped[str] = mapped_column(String(32), nullable=False)
    min_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    max_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    raw_data: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    synced_at: Mapped[datetime] = mapped_column(nullable=False)


class Currency(UUIDPKMixin, Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    country_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("countries.id", ondelete="SET NULL"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
