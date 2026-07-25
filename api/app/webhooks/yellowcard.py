import logging

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.webhook_processing_service import process_yellowcard_webhook

logger = logging.getLogger("app.webhooks")

router = APIRouter(prefix="/internal/webhooks", tags=["webhooks"])


@router.post("/yellowcard")
async def receive_yellowcard_webhook(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    """Point de reception unique des webhooks Yellow Card. Repond toujours 200
    rapidement (l'evenement est persiste avant tout traitement) pour eviter les
    tempetes de retry cote Yellow Card en cas d'echec de traitement local.

    Le corps brut (bytes exacts) est indispensable pour la verification de
    signature X-YC-Signature - ne pas le re-serialiser via request.json()."""
    raw_body = await request.body()
    headers = {k.lower(): v for k, v in request.headers.items()}

    event = await process_yellowcard_webhook(db, raw_body=raw_body, headers=headers)
    return {"received": True, "event_id": str(event.id), "status": event.status.value}
