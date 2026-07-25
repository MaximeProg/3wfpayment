import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPKMixin
from app.models.enums import StatusChangeSource, TransactionStatus, TransactionType


class Transaction(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint("project_id", "client_reference", name="uq_transactions_project_client_ref"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True
    )
    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type"), nullable=False, index=True
    )
    reference: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    client_reference: Mapped[str | None] = mapped_column(String(120), nullable=True)
    yellowcard_reference: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, name="transaction_status"),
        default=TransactionStatus.pending,
        nullable=False,
        index=True,
    )
    # Numeric(24, 8) : les montants crypto (crypto_send) ont besoin de plus de
    # decimales que les montants fiat (ex. 5.40642173 USDT).
    amount: Mapped[Decimal] = mapped_column(Numeric(24, 8), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(8), nullable=False)
    country_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("countries.id"), nullable=True
    )
    network_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("networks.id"), nullable=True
    )
    customer_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    request_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    response_payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    failure_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    initiated_at: Mapped[datetime] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    status_history: Mapped[list["TransactionStatusHistory"]] = relationship(
        back_populates="transaction", order_by="TransactionStatusHistory.created_at"
    )


class TransactionStatusHistory(UUIDPKMixin, Base):
    __tablename__ = "transaction_status_history"

    transaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("transactions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    previous_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    new_status: Mapped[str] = mapped_column(String(32), nullable=False)
    source: Mapped[StatusChangeSource] = mapped_column(
        Enum(StatusChangeSource, name="status_change_source"), nullable=False
    )
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    transaction: Mapped["Transaction"] = relationship(back_populates="status_history")
