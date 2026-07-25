"""Mapping des statuts Yellow Card (Send/Receive) vers nos statuts internes.
Partage entre le polling (transaction_service) et le traitement des webhooks."""

import logging

from app.models.enums import TransactionStatus

logger = logging.getLogger("app.transactions")

# Statuts Yellow Card observes dans la doc (created, complete) + statuts probables
# pour les flux deny/cancel/fail/refund. Toute valeur non reconnue est mappee sur
# "processing" par defaut (fail-safe : jamais "completed" par defaut) et journalisee.
_STATUS_MAP: dict[str, TransactionStatus] = {
    "created": TransactionStatus.pending,
    "pending": TransactionStatus.pending,
    "processing": TransactionStatus.processing,
    "complete": TransactionStatus.completed,
    "completed": TransactionStatus.completed,
    "failed": TransactionStatus.failed,
    "denied": TransactionStatus.failed,
    "cancelled": TransactionStatus.cancelled,
    "canceled": TransactionStatus.cancelled,
    "expired": TransactionStatus.expired,
    "refunded": TransactionStatus.failed,
}


def map_status(raw_status: str | None) -> TransactionStatus:
    if not raw_status:
        return TransactionStatus.processing
    mapped = _STATUS_MAP.get(raw_status.lower())
    if mapped is None:
        logger.warning("Statut Yellow Card non reconnu : %r (mappe sur 'processing')", raw_status)
        return TransactionStatus.processing
    return mapped


def is_terminal(status: TransactionStatus) -> bool:
    return status in (
        TransactionStatus.completed,
        TransactionStatus.failed,
        TransactionStatus.cancelled,
        TransactionStatus.expired,
    )
