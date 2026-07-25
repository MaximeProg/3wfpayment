| Code | Cas | Corps |
|---|---|---|
| `401` | Token manquant, invalide ou expire | `{"detail": "Token invalide"}` ou `{"detail": "Token manquant"}` |
| `401` | Cle API invalide/revoquee (sur `/v1/auth/token`) | `{"detail": "Cle API invalide ou revoquee"}` |
| `403` | Scope manquant sur le token | `{"detail": "Scope manquant : 'crypto_sends:write'"}` |
| `404` | Transaction introuvable ou n'appartenant pas a votre projet | `{"detail": "Transaction introuvable"}` |
| `422` | Corps de requete invalide (champ manquant/mal type) | `{"detail": [{"type": "missing", "loc": ["body", "customer_uid"], "msg": "Field required"}, ...]}` (format standard FastAPI/Pydantic — une entree par champ en erreur) |
| `422` | `channel_id`/`network_id` non resolu | `{"detail": "..."}` |
| `502` | Yellow Card a rejete la requete | `{"detail": {"message": "Yellow Card a rejete la requete de depot", "yellowcard_error": {"code": "...", "message": "..."}}}` — inspectez `yellowcard_error` pour la cause exacte (ex. format de telephone, montant hors plage, channel indisponible). |

Sur un `502`, la transaction **n'a pas ete creee** cote Payment Platform — vous pouvez corriger et retenter avec le meme `client_reference` sans risque de doublon (voir [Idempotence](/docs/transactions#idempotence)).
