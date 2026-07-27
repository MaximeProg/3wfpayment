"""Livraison des notifications de changement de statut aux projets clients
(webhook sortant). Best-effort : ne doit jamais lever, ni bloquer le flux
appelant (webhook entrant Yellow Card ou polling de secours).

Format du payload : identique a TransactionOut (schema deja expose sur
GET /v1/transactions/{id}), signe en base64(HMAC-SHA256(secret, corps_brut))
- meme scheme que la signature Yellow Card entrante, applique en sortie.
Header : X-Payment-Platform-Signature.
"""

import json
import logging

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decrypt_secret
from app.integrations.yellowcard.webhook_signature import compute_webhook_signature
from app.models.enums import ErrorLevel, ErrorSource
from app.models.project import Project
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionOut
from app.services.error_log_service import log_error

logger = logging.getLogger("app.webhooks.outbound")


async def deliver_status_update(db: AsyncSession, transaction: Transaction) -> None:
    # Requete explicite plutot que `transaction.project` : evite le lazy-load
    # implicite (non supporte hors contexte greenlet en SQLAlchemy async) aux
    # points d'appel qui n'eager-load pas la relation.
    project = await db.get(Project, transaction.project_id)
    if project is None or not project.webhook_url or not project.webhook_secret_encrypted:
        return

    secret = decrypt_secret(project.webhook_secret_encrypted)
    body = TransactionOut.model_validate(transaction).model_dump(mode="json")
    raw_body = json.dumps(body).encode("utf-8")
    signature = compute_webhook_signature(secret, raw_body)

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                project.webhook_url,
                content=raw_body,
                headers={
                    "Content-Type": "application/json",
                    "X-Payment-Platform-Signature": signature,
                },
            )
            response.raise_for_status()
        logger.info(
            "Webhook sortant livre : projet=%s transaction=%s statut=%s",
            project.slug,
            transaction.id,
            transaction.status.value,
        )
    except httpx.HTTPError as exc:
        logger.warning(
            "Echec de livraison du webhook sortant pour le projet %s (transaction %s) : %s",
            project.slug,
            transaction.id,
            exc,
        )
        await log_error(
            db,
            source=ErrorSource.webhook,
            level=ErrorLevel.warning,
            message=f"Echec de livraison du webhook sortant vers {project.slug}",
            context={
                "project_id": str(project.id),
                "transaction_id": str(transaction.id),
                "webhook_url": project.webhook_url,
                "error": str(exc),
            },
        )
