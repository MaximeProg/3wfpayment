Un depot = un utilisateur final envoie de l'argent vers le wallet Yellow Card du produit (cash-in).

## `POST /v1/deposits` — scope `deposits:write`

```bash
curl -X POST "https://threewfpayment.onrender.com/v1/deposits" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "client_reference": "doc-example-dep-003",
    "customer_uid": "doc-user-001",
    "customer_type": "retail",
    "local_amount": 1000,
    "currency": "KES",
    "channel_id": "96ee8110-d1c2-4606-8d27-05c2aa6a4f98",
    "source_account_type": "momo",
    "source_account_number": "+254712345678",
    "source_network_id": "19fc0dd0-0da7-4050-9ab6-8b7d05ed5ccd",
    "recipient": {"name": "Jane Doe", "country": "KE", "phone": "+254712345678"},
    "reason": "other",
    "force_accept": true
  }'
```

Corps complet de la requete :

```json
{
  "client_reference": "doc-example-dep-003",
  "customer_uid": "doc-user-001",
  "customer_type": "retail",
  "local_amount": 1000,
  "currency": "KES",
  "channel_id": "96ee8110-d1c2-4606-8d27-05c2aa6a4f98",
  "source_account_type": "momo",
  "source_account_number": "+254712345678",
  "source_network_id": "19fc0dd0-0da7-4050-9ab6-8b7d05ed5ccd",
  "recipient": {
    "name": "Jane Doe",
    "country": "KE",
    "phone": "+254712345678",
    "address": "Nairobi",
    "dob": "01/15/1990",
    "email": "jane.doe@example.com",
    "id_number": "12345678",
    "id_type": "national_id"
  },
  "reason": "other",
  "force_accept": true
}
```

Reponse `201` :

```json
{
  "id": "5a705bf9-e8a5-42f8-b886-14134440283d",
  "type": "deposit",
  "reference": "DEP-5972aa646338462b",
  "client_reference": "doc-example-dep-003",
  "yellowcard_reference": "ab18cee8-717d-53c6-92d2-e69a000348f2",
  "status": "processing",
  "amount": "1000.00000000",
  "currency_code": "KES",
  "failure_reason": null,
  "initiated_at": "2026-07-25T15:01:42Z",
  "completed_at": null,
  "created_at": "2026-07-25T15:01:37Z",
  "updated_at": "2026-07-25T15:01:37Z"
}
```

### Champs cles

| Champ | Description |
|---|---|
| `client_reference` | Votre cle d'idempotence (unique par projet). Rejouer le meme appel avec la meme valeur renvoie la transaction existante au lieu d'en creer une nouvelle — voir [Statuts & transactions](/docs/transactions). |
| `customer_uid` | Identifiant de l'utilisateur dans **votre** systeme (pas transmis tel quel a Yellow Card, sert a votre tracabilite). |
| `local_amount` | Montant en devise locale, **entier sans decimales** (Yellow Card l'exige). |
| `channel_id` / `source_network_id` | Resolus via [Donnees de reference](/docs/reference-data) — jamais un ID Yellow Card brut. |
| `source_account_number` | Numero de telephone (momo) ou de compte (bank) du payeur. **Format international requis pour les numeros de telephone** (ex. `+254712345678`, pas `254712345678` — Yellow Card rejette le format national, voir l'erreur type ci-dessous). |
| `recipient` | KYC minimal du titulaire du wallet destinataire. Les champs requis varient selon `customer_type` et le pays — en cas de doute, remplissez-les tous. |
| `force_accept` | Laissez `true` sauf besoin specifique (evite un etat intermediaire "a confirmer manuellement" cote Yellow Card). |

### Erreur reelle rencontree en sandbox

Numero de telephone sans indicatif international :

```json
{
  "detail": {
    "message": "Yellow Card a rejete la requete de depot",
    "yellowcard_error": {
      "code": "InvalidPhoneNumberFormat",
      "message": "phone number needs to be in international format: 254712345678"
    }
  }
}
```

→ HTTP `502`. Voir [Erreurs](/docs/errors) pour le detail des codes.

## `GET /v1/deposits/{id}` et `GET /v1/deposits` — scope `transactions:read`

```bash
curl "https://threewfpayment.onrender.com/v1/deposits/5a705bf9-e8a5-42f8-b886-14134440283d" \
  -H "Authorization: Bearer <token>"
```

`GET /v1/deposits/{id}` declenche automatiquement un rafraichissement du statut aupres de Yellow Card si la transaction n'est pas encore dans un etat terminal (voir [Statuts & transactions](/docs/transactions)) — c'est le mecanisme de secours en l'absence de webhook.

```bash
curl "https://threewfpayment.onrender.com/v1/deposits?status=completed&limit=50&offset=0" \
  -H "Authorization: Bearer <token>"
```

Liste les depots du projet, filtrable par `status`.
