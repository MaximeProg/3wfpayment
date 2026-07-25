Un retrait = le produit envoie de l'argent depuis le wallet Yellow Card vers un utilisateur final (cash-out). Meme logique que les [depots](/docs/deposits), avec `destination_*` au lieu de `source_*` et `sender` au lieu de `recipient`.

## `POST /v1/withdrawals` — scope `withdrawals:write`

```json
{
  "client_reference": "doc-example-wdr-001",
  "customer_uid": "doc-user-001",
  "customer_type": "retail",
  "local_amount": 500,
  "currency": "KES",
  "channel_id": "b00b21eb-7fa2-417d-b558-ed108ae2ba1d",
  "reason": "other",
  "destination_account_type": "momo",
  "destination_account_number": "+254712345678",
  "destination_account_name": "Jane Doe",
  "destination_network_id": "19fc0dd0-0da7-4050-9ab6-8b7d05ed5ccd",
  "sender": {
    "name": "Jane Doe",
    "country": "KE",
    "phone": "+254712345678",
    "address": "Nairobi",
    "dob": "01/15/1990",
    "email": "jane.doe@example.com",
    "id_number": "12345678",
    "id_type": "national_id"
  },
  "force_accept": true
}
```

Reponse `201` :

```json
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
}
```

`reason` est **requis** pour un retrait (contrairement au depot ou il a une valeur par defaut). `GET /v1/withdrawals/{id}` et `GET /v1/withdrawals` fonctionnent comme pour les depots (voir [Statuts & transactions](/docs/transactions)).
