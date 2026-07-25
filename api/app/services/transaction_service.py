import logging
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.yellowcard.client import YellowCardAPIError
from app.integrations.yellowcard.crypto import lookup_crypto_send_by_sequence_id, submit_crypto_send
from app.integrations.yellowcard.transactions import (
    lookup_receive,
    lookup_send,
    submit_receive,
    submit_send,
)
from app.models.enums import (
    AdminRole,
    ErrorLevel,
    ErrorSource,
    NotificationCategory,
    StatusChangeSource,
    TransactionStatus,
    TransactionType,
)
from app.models.project import Project
from app.models.reference_data import Channel, Network
from app.models.transaction import Transaction
from app.repositories import reference_data_repository as reference_repo
from app.repositories import transaction_repository as repo
from app.schemas.transaction import CryptoSendCreateRequest, DepositCreateRequest, WithdrawalCreateRequest
from app.services.error_log_service import log_error
from app.services.notification_service import notify
from app.services.yellowcard_credentials_service import build_client
from app.services.yellowcard_status_mapping import is_terminal, map_status

logger = logging.getLogger("app.transactions")


class ChannelNotFoundError(Exception):
    pass


class NetworkNotFoundError(Exception):
    pass


async def _resolve_channel(db: AsyncSession, channel_id: uuid.UUID) -> Channel:
    channel = await reference_repo.get_channel_by_id(db, channel_id)
    if channel is None:
        raise ChannelNotFoundError(f"Channel introuvable : {channel_id}")
    return channel


async def _resolve_network(db: AsyncSession, network_id: uuid.UUID) -> Network:
    network = await reference_repo.get_network_by_id(db, network_id)
    if network is None:
        raise NetworkNotFoundError(f"Network introuvable : {network_id}")
    return network


def _new_reference(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:16]}"


async def create_deposit(db: AsyncSession, *, project: Project, payload: DepositCreateRequest) -> Transaction:
    existing = await repo.get_by_client_reference(
        db, project_id=project.id, client_reference=payload.client_reference
    )
    if existing is not None:
        return existing

    channel = await _resolve_channel(db, payload.channel_id)
    source_network = (
        await _resolve_network(db, payload.source_network_id) if payload.source_network_id else None
    )

    reference = _new_reference("DEP")
    body: dict[str, Any] = {
        "sequenceId": reference,
        "customerUID": payload.customer_uid,
        "customerType": payload.customer_type,
        "localAmount": int(payload.local_amount),
        "currency": payload.currency,
        "channelId": channel.yellowcard_id,
        "source": {
            "accountType": payload.source_account_type,
            "accountNumber": payload.source_account_number,
            **({"networkId": source_network.yellowcard_id} if source_network else {}),
        },
        "recipient": payload.recipient.model_dump(exclude_none=True),
        "reason": payload.reason,
        "forceAccept": payload.force_accept,
    }

    client = await build_client(db, environment=project.environment)
    response = await submit_receive(client, body)

    now = datetime.now(timezone.utc)
    status = map_status(response.get("status"))

    transaction = Transaction(
        project_id=project.id,
        type=TransactionType.deposit,
        reference=reference,
        client_reference=payload.client_reference,
        yellowcard_reference=response.get("id"),
        status=status,
        amount=Decimal(str(response.get("convertedAmount", payload.local_amount))),
        currency_code=payload.currency,
        customer_payload=payload.recipient.model_dump(exclude_none=True),
        request_payload=body,
        response_payload=response,
        initiated_at=now,
        completed_at=now if is_terminal(status) else None,
    )
    transaction = await repo.create(db, transaction)
    await notify(
        db,
        category=NotificationCategory.transaction,
        audience_min_role=AdminRole.super_admin,
        title="Nouveau depot initie",
        message=f"{transaction.amount} {transaction.currency_code} — projet {project.name}",
        related_type="transaction",
        related_id=str(transaction.id),
    )
    return transaction


async def create_withdrawal(
    db: AsyncSession, *, project: Project, payload: WithdrawalCreateRequest
) -> Transaction:
    existing = await repo.get_by_client_reference(
        db, project_id=project.id, client_reference=payload.client_reference
    )
    if existing is not None:
        return existing

    channel = await _resolve_channel(db, payload.channel_id)
    destination_network = await _resolve_network(db, payload.destination_network_id)

    reference = _new_reference("WDR")
    body: dict[str, Any] = {
        "sequenceId": reference,
        "customerUID": payload.customer_uid,
        "customerType": payload.customer_type,
        "localAmount": int(payload.local_amount),
        "currency": payload.currency,
        "channelId": channel.yellowcard_id,
        "reason": payload.reason,
        "destination": {
            "accountType": payload.destination_account_type,
            "accountNumber": payload.destination_account_number,
            "accountName": payload.destination_account_name,
            "networkId": destination_network.yellowcard_id,
        },
        "sender": payload.sender.model_dump(exclude_none=True),
        "forceAccept": payload.force_accept,
    }

    client = await build_client(db, environment=project.environment)
    response = await submit_send(client, body)

    now = datetime.now(timezone.utc)
    status = map_status(response.get("status"))

    transaction = Transaction(
        project_id=project.id,
        type=TransactionType.withdrawal,
        reference=reference,
        client_reference=payload.client_reference,
        yellowcard_reference=response.get("id"),
        status=status,
        amount=Decimal(str(response.get("convertedAmount", payload.local_amount))),
        currency_code=payload.currency,
        customer_payload=payload.sender.model_dump(exclude_none=True),
        request_payload=body,
        response_payload=response,
        initiated_at=now,
        completed_at=now if is_terminal(status) else None,
    )
    transaction = await repo.create(db, transaction)
    await notify(
        db,
        category=NotificationCategory.transaction,
        audience_min_role=AdminRole.super_admin,
        title="Nouveau retrait initie",
        message=f"{transaction.amount} {transaction.currency_code} — projet {project.name}",
        related_type="transaction",
        related_id=str(transaction.id),
    )
    return transaction


async def create_crypto_send(
    db: AsyncSession, *, project: Project, payload: CryptoSendCreateRequest
) -> Transaction:
    existing = await repo.get_by_client_reference(
        db, project_id=project.id, client_reference=payload.client_reference
    )
    if existing is not None:
        return existing

    reference = _new_reference("CRY")
    # Le schema Yellow Card documente "amount" comme un entier, mais les exemples
    # reels de reponses montrent des montants crypto fractionnaires acceptes -
    # on envoie un int quand c'est un montant rond, un float sinon.
    is_whole = payload.amount == payload.amount.to_integral_value()
    amount_value: int | float = int(payload.amount) if is_whole else float(payload.amount)

    body: dict[str, Any] = {
        "sequenceId": reference,
        "amount": amount_value,
        "walletAddress": payload.wallet_address,
        "cryptoCurrency": payload.crypto_currency,
        "cryptoNetwork": payload.crypto_network,
        "travelRuleInfo": {
            "name": payload.travel_rule_name,
            "businessRegistrationNumber": payload.travel_rule_business_registration_number,
        },
    }

    client = await build_client(db, environment=project.environment)
    response = await submit_crypto_send(client, body)

    now = datetime.now(timezone.utc)
    status = map_status(response.get("status"))

    transaction = Transaction(
        project_id=project.id,
        type=TransactionType.crypto_send,
        reference=reference,
        client_reference=payload.client_reference,
        yellowcard_reference=response.get("id"),
        status=status,
        amount=Decimal(str(response.get("cryptoAmount", payload.amount))),
        currency_code=payload.crypto_currency,
        customer_payload={"customer_uid": payload.customer_uid} if payload.customer_uid else {},
        request_payload=body,
        response_payload=response,
        initiated_at=now,
        completed_at=now if is_terminal(status) else None,
    )
    return await repo.create(db, transaction)


async def refresh_transaction_status(db: AsyncSession, *, project: Project, transaction: Transaction) -> Transaction:
    """Interroge Yellow Card pour rafraichir le statut (polling de secours, en
    complement des webhooks - cf. plan technique section 9)."""
    if is_terminal(transaction.status):
        return transaction

    client = await build_client(db, environment=project.environment)
    try:
        if transaction.type == TransactionType.crypto_send:
            # Le lookup crypto se fait par sequenceId (notre reference), pas par
            # l'id Yellow Card - a la difference de /send et /receive.
            response = await lookup_crypto_send_by_sequence_id(client, transaction.reference)
        elif not transaction.yellowcard_reference:
            return transaction
        elif transaction.type == TransactionType.deposit:
            response = await lookup_receive(client, transaction.yellowcard_reference)
        else:
            response = await lookup_send(client, transaction.yellowcard_reference)
    except YellowCardAPIError as exc:
        logger.exception("Echec du lookup Yellow Card pour la transaction %s", transaction.id)
        await log_error(
            db,
            source=ErrorSource.yellowcard_api,
            level=ErrorLevel.warning,
            message=f"Echec du lookup de statut pour la transaction {transaction.reference}",
            context={"status_code": exc.status_code, "payload": exc.payload, "transaction_id": str(transaction.id)},
        )
        return transaction

    status = map_status(response.get("status"))
    now = datetime.now(timezone.utc) if is_terminal(status) else None

    return await repo.update_status(
        db,
        transaction,
        new_status=status,
        response_payload=response,
        failure_reason=response.get("message") if status == TransactionStatus.failed else None,
        completed_at=now,
        source=StatusChangeSource.polling,
    )
