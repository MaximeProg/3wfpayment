Payment Platform n'utilise **pas OAuth**. Le flux est :

1. Vous detenez une cle API complete (`pp_<prefix>_<secret>`), obtenue une seule fois a la creation ([Obtenir un projet et une cle API](/docs/getting-started)).
2. Vous l'echangez contre un **token JWT court** via `POST /v1/auth/token`.
3. Vous utilisez ce token en `Authorization: Bearer <token>` sur tous les appels `/v1/*` suivants.
4. Le token expire au bout de **15 minutes** (`expires_in: 900`) — re-echangez votre cle API pour en obtenir un nouveau. Ne cachez pas le token plus longtemps ; re-echangez proactivement (ex. des qu'il reste moins d'une minute) plutot que d'attendre un `401`.

```http
POST /v1/auth/token
Content-Type: application/json

{"api_key": "pp_<prefix>_<secret>"}
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 900
}
```

Un token invalide, mal forme ou expire renvoie `401` sur n'importe quel endpoint `/v1/*` :

```json
{"detail": "Token invalide"}
```

Une cle API invalide ou revoquee renvoie `401` des l'echange :

```json
{"detail": "Cle API invalide ou revoquee"}
```
