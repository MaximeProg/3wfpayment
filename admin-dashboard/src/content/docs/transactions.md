## Statuts

Statuts possibles (champ `status` sur une transaction) :

| Statut | Sens |
|---|---|
| `pending` | Creee, pas encore traitee par Yellow Card. |
| `processing` | En cours de traitement. |
| `completed` | **Terminal.** Fonds arrives. |
| `failed` | **Terminal.** Echec (voir `failure_reason` si present). |
| `cancelled` | **Terminal.** Annulee. |
| `expired` | **Terminal.** Expiree avant completion. |

## Comment suivre une transaction

**Il n'y a actuellement aucun webhook sortant depuis Payment Platform vers les projets consommateurs.** Payment Platform recoit lui-meme les webhooks de Yellow Card et les applique en interne, mais ne les retransmet pas encore a votre produit. Pour suivre l'evolution d'une transaction, vous devez **poller** :

- `GET /v1/{deposits|withdrawals|crypto-sends|transactions}/{id}` rafraichit activement le statut aupres de Yellow Card si la transaction n'est pas dans un etat terminal (l'appel peut donc etre legerement plus lent qu'un simple GET tant que le statut n'est pas final).
- Une fois `status` dans un etat terminal, il ne changera plus — vous pouvez arreter de poller.
- Frequence recommandee : quelques secondes a quelques dizaines de secondes apres creation, avec backoff progressif si l'etat reste `pending`/`processing` longtemps.

Si votre produit a besoin de notifications push (webhook sortant) plutot que du polling, remontez ce besoin a [l'equipe plateforme](/docs/resources) — ce n'est pas encore construit.

## Idempotence

`client_reference` est votre cle d'idempotence, **unique par projet** (deux projets differents peuvent reutiliser la meme valeur sans collision). Si vous rejouez un `POST /v1/deposits` ou `POST /v1/withdrawals` avec un `client_reference` deja vu, Payment Platform renvoie la transaction existante (meme code `201`, pas d'erreur, pas de nouvelle transaction creee) au lieu de re-soumettre la requete a Yellow Card. Utilisez systematiquement un identifiant stable genere une seule fois par intention de paiement cote client (pas un timestamp ou un UUID regenere a chaque retry).

## Pagination

Les endpoints de liste (`GET /v1/deposits`, `/v1/withdrawals`, `/v1/crypto-sends`, `/v1/transactions`) acceptent `limit` (defaut 50, max 200) et `offset` (defaut 0). Il n'y a pas de curseur ni de total count dans la reponse — utilisez `limit`/`offset` classiques et arretez de paginer quand une page revient plus courte que `limit`.

## Exemple : liste des transactions d'un projet

```bash
curl "https://threewfpayment.onrender.com/v1/transactions?limit=10" \
  -H "Authorization: Bearer <token>"
```

```json
[
  {
    "id": "6aadc33d-834a-4a51-8f87-4fbcbb4772de",
    "type": "withdrawal",
    "reference": "WDR-52078d2869a94870",
    "client_reference": "doc-example-wdr-001",
    "yellowcard_reference": "c6317f74-65d6-5d6f-877e-5a6f461d9a4b",
    "status": "pending",
    "amount": "500.00000000",
    "currency_code": "KES",
    "failure_reason": null,
    "initiated_at": "2026-07-25T15:20:48Z",
    "completed_at": null,
    "created_at": "2026-07-25T15:20:36Z",
    "updated_at": "2026-07-25T15:20:36Z"
  },
  {
    "id": "5a705bf9-e8a5-42f8-b886-14134440283d",
    "type": "deposit",
    "reference": "DEP-5972aa646338462b",
    "client_reference": "doc-example-dep-003",
    "yellowcard_reference": "ab18cee8-717d-53c6-92d2-e69a000348f2",
    "status": "failed",
    "amount": "1000.00000000",
    "currency_code": "KES",
    "failure_reason": null,
    "initiated_at": "2026-07-25T15:01:42Z",
    "completed_at": "2026-07-25T15:03:22Z",
    "created_at": "2026-07-25T15:01:37Z",
    "updated_at": "2026-07-25T15:03:19Z"
  }
]
```
