import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # Toute colonne "Mapped[datetime]" est timezone-aware par defaut (TIMESTAMPTZ) :
    # evite les erreurs asyncpg "offset-naive vs offset-aware" quand on ecrit des
    # datetime.now(timezone.utc) dans une colonne declaree sans type explicite.
    type_annotation_map = {datetime: DateTime(timezone=True)}


class UUIDPKMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
