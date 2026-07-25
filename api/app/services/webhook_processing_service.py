"""Traitement des webhooks entrants Yellow Card.

Format confirme par la doc Yellow Card ("Webhooks") :
{
  "id": "...",              # reference Yellow Card (Transaction.yellowcard_reference)
  "sequenceId": "...",      # notre reference (Transaction.reference)
  "status": "failed",       # statut brut Yellow Card
  "apiKey": "...",          # identifie quel credential (sandbox/production) a signe
  "event": "RECEIVE.FAILED",# <RECEIVE|SEND|CRYPTO_SEND|CRYPTO_RECEIVE|CONVERT>.<STATE>
  "errorCode": "REFUSED",   # present uniquement en cas d'echec
  "sessionId": "...",
  "executedAt": "2023-02-20T14:25:30.459Z"
}

Authenticite : header X-YC-Signature = base64(HMAC-SHA256(secret, corps_brut)).
Le corps brut (bytes exacts recus, avant tout reserialisation JSON) est requis
pour que le hash corresponde - cf. app/webhooks/yellowcard.py.

Posture : si la signature ne peut pas etre verifiee (header absent, ou aucun
credential ne matche), l'evenement est quand meme persiste (raw payload complet)
pour investigation, mais AUCUNE mise a jour de transaction n'est appliquee a
partir de son contenu - seul un webhook signe est source de verite. Le polling de
secours (transaction_service.refresh_transaction_status) reste disponible.
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AdminRole, ErrorLevel, ErrorSource, NotificationCategory, StatusChangeSource
from app.models.webhook import WebhookEvent
from app.repositories import transaction_repository
from app.repositories import webhook_repository as repo
from app.services.error_log_service import log_error
from app.services.notification_service import notify
from app.services.yellowcard_credentials_service import verify_webhook_and_resolve_environment
from app.services.yellowcard_status_mapping import is_terminal, map_status

logger = logging.getLogger("app.webhooks")


def _build_external_event_id(payload: dict[str, Any]) -> str:
    basis = "|".join(
        str(payload.get(k, "")) for k in ("id", "event", "status", "executedAt", "sessionId")
    )
    if basis.strip("|") == "":
        basis = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


async def _apply_to_transaction(db: AsyncSession, event: WebhookEvent, raw_payload: dict[str, Any]) -> WebhookEvent:
    yc_id = raw_payload.get("id")
    if not yc_id:
        return await repo.mark_failed(db, event, error="Champ 'id' absent du payload")

    transaction = await transaction_repository.get_by_yellowcard_reference(db, yc_id)
    if transaction is None:
        return await repo.mark_failed(
            db, event, error=f"Aucune transaction locale pour la reference Yellow Card '{yc_id}'"
        )

    raw_status = raw_payload.get("status")
    status = map_status(raw_status)
    now = datetime.now(timezone.utc) if is_terminal(status) else None

    await transaction_repository.update_status(
        db,
        transaction,
        new_status=status,
        response_payload=raw_payload,
        failure_reason=raw_payload.get("errorCode") if status.value == "failed" else None,
        completed_at=now,
        source=StatusChangeSource.webhook,
    )

    if status.value in ("completed", "failed"):
        await notify(
            db,
            category=NotificationCategory.transaction,
            audience_min_role=AdminRole.super_admin,
            title="Transaction terminee" if status.value == "completed" else "Transaction echouee",
            message=f"{transaction.reference} — {transaction.amount} {transaction.currency_code}",
            related_type="transaction",
            related_id=str(transaction.id),
        )

    return await repo.mark_processed(db, event, transaction_id=transaction.id)


async def process_yellowcard_webhook(
    db: AsyncSession, *, raw_body: bytes, headers: dict[str, str]
) -> WebhookEvent:
    try:
        raw_payload: dict[str, Any] = json.loads(raw_body)
    except ValueError:
        raw_payload = {}

    external_event_id = _build_external_event_id(raw_payload)

    existing = await repo.get_by_external_event_id(db, external_event_id)
    if existing is not None:
        return existing

    signature_header = headers.get("x-yc-signature")
    environment = await verify_webhook_and_resolve_environment(
        db,
        raw_body=raw_body,
        signature_header=signature_header,
        api_key_hint=raw_payload.get("apiKey"),
    )
    signature_valid = environment is not None

    event = await repo.create(
        db,
        event_type=str(raw_payload.get("event", "unknown")),
        external_event_id=external_event_id,
        signature_valid=signature_valid,
        raw_payload=raw_payload,
    )

    if not signature_valid:
        logger.warning("Webhook Yellow Card recu avec une signature invalide ou absente")
        await log_error(
            db,
            source=ErrorSource.webhook,
            level=ErrorLevel.warning,
            message="Webhook Yellow Card recu avec une signature invalide ou absente",
            context={"event_id": str(event.id), "has_signature_header": bool(signature_header)},
        )
        return await repo.mark_failed(db, event, error="Signature X-YC-Signature invalide ou absente")

    return await _apply_to_transaction(db, event, raw_payload)


async def reprocess_webhook_event(db: AsyncSession, event: WebhookEvent) -> WebhookEvent:
    """Retraitement manuel declenche par un admin (ex: la transaction n'existait
    pas encore au moment de la reception initiale). N'effectue pas de nouvelle
    verification de signature - action explicite et tracee (audit log cote
    routeur), sur un evenement deja persiste."""
    return await _apply_to_transaction(db, event, event.raw_payload)
