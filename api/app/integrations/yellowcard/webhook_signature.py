"""Verification de la signature des webhooks entrants Yellow Card.

D'apres la doc Yellow Card ("Webhooks" - page recipe) :
- header X-YC-Signature
- signature = base64(HMAC-SHA256(secretKey, corps_brut_de_la_requete))
- le champ "apiKey" present dans le payload identifie quelle cle/secret utiliser
"""

import base64
import hashlib
import hmac


def compute_webhook_signature(secret: str, raw_body: bytes) -> str:
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def verify_webhook_signature(secret: str, raw_body: bytes, signature_header: str) -> bool:
    if not signature_header:
        return False
    expected = compute_webhook_signature(secret, raw_body)
    return hmac.compare_digest(expected, signature_header)
