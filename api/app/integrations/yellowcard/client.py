"""Client HTTP pour l'API Business de Yellow Card.

Authentification : signature HMAC-SHA256 par requete (schema `YcHmacV1`), telle que
documentee sur https://docs.yellowcard.engineering/docs/authentication-api.
Il n'y a pas de jeton OAuth a obtenir ni a renouveler : chaque requete est signee
individuellement avec la cle API et le secret.

Chaine signee (dans cet ordre exact) :
    timestamp (ISO8601 + "Z") + path (ex: "/business/channels") + method (ex: "GET")
    [+ base64(sha256(json.dumps(body))) si un corps est fourni]

Note : l'exemple officiel Yellow Card (page Authentication) n'inclut le hash du
corps que si `len(body) > 1`. Ce comportement ne correspond PAS a la verification
reelle du serveur : confirme le 24/07/2026 sur POST /vaults (corps a une seule
cle, `{"name": ...}`), qui echoue en 401 "invalid apiKey signature combination"
avec la regle `len(body) > 1`, et reussit (201) des que le corps est inclus dans
la signature sans condition sur le nombre de cles.

Le corps de la requete, quand il est envoye, doit etre exactement la meme serialisation
JSON que celle utilisee pour la signature (d'ou l'encodage manuel plutot que de laisser
httpx serialiser le JSON lui-meme).
"""

import base64
import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any

import httpx

from app.core.config import get_settings

API_PREFIX = "/business"


class YellowCardAPIError(Exception):
    def __init__(self, status_code: int, payload: Any):
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"Yellow Card API error {status_code}: {payload!r}")


class YellowCardClient:
    def __init__(self, *, api_key: str, api_secret: str, base_url: str | None = None):
        if not api_key or not api_secret:
            raise ValueError("api_key et api_secret sont requis pour signer les requetes Yellow Card")
        self._api_key = api_key
        self._api_secret = api_secret.encode("utf-8")
        settings = get_settings()
        self._base_url = (base_url or settings.yellowcard_base_url).rstrip("/")

    def _sign(self, *, path: str, method: str, body: dict | None) -> dict[str, str]:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

        hmac_object = hmac.new(key=self._api_secret, digestmod=hashlib.sha256)
        hmac_object.update(timestamp.encode("utf-8"))
        hmac_object.update(path.encode("utf-8"))
        hmac_object.update(method.encode("utf-8"))

        if body:
            body_json = json.dumps(body)
            body_hash = base64.b64encode(hashlib.sha256(body_json.encode("utf-8")).digest()).decode("utf-8")
            hmac_object.update(body_hash.encode("utf-8"))

        signature = base64.b64encode(hmac_object.digest()).decode("utf-8")

        return {
            "X-YC-Timestamp": timestamp,
            "Authorization": f"YcHmacV1 {self._api_key}:{signature}",
        }

    @staticmethod
    def _parse_response(response: httpx.Response) -> Any:
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        timeout: float = 30.0,
    ) -> Any:
        path = f"{API_PREFIX}{endpoint}"
        method_upper = method.upper()

        headers = self._sign(path=path, method=method_upper, body=body)

        content: bytes | None = None
        if body is not None:
            content = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        url = f"{self._base_url}{path}"

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(method_upper, url, headers=headers, params=params, content=content)

        payload = self._parse_response(response)
        if response.status_code // 100 != 2:
            raise YellowCardAPIError(response.status_code, payload)
        return payload

    async def get(self, endpoint: str, *, params: dict[str, Any] | None = None, timeout: float = 30.0) -> Any:
        return await self.request("GET", endpoint, params=params, timeout=timeout)

    async def post(self, endpoint: str, *, body: dict[str, Any] | None = None) -> Any:
        return await self.request("POST", endpoint, body=body)

    async def put(self, endpoint: str, *, body: dict[str, Any] | None = None) -> Any:
        return await self.request("PUT", endpoint, body=body)

    async def delete(self, endpoint: str) -> Any:
        return await self.request("DELETE", endpoint)
