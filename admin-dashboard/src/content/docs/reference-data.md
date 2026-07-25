Avant de creer un depot ou un retrait, vous devez resoudre les identifiants Payment Platform (des UUID internes — **pas** les identifiants Yellow Card bruts) via ces endpoints. Ils sont synchronises regulierement depuis Yellow Card ; ne codez jamais un UUID en dur dans votre application, resolvez-le a chaque fois (ou cachez-le avec une expiration courte).

Tous les endpoints ci-dessous necessitent le header `Authorization: Bearer <token>` (voir [Authentification](/docs/authentication)).

## `GET /v1/countries`

```bash
curl "https://threewfpayment.onrender.com/v1/countries" \
  -H "Authorization: Bearer <token>"
```

```json
[
  {"id": "b661bb73-fcbf-45cb-b317-79db87a1b3d2", "iso_code": "KE", "name": "Kenya", "is_active": true, "synced_at": "2026-07-24T18:23:01Z"}
]
```

## `GET /v1/networks`

Un "reseau" est une banque ou un operateur mobile money precis (ex. M-PESA au Kenya).

```bash
curl "https://threewfpayment.onrender.com/v1/networks" \
  -H "Authorization: Bearer <token>"
```

```json
[
  {"id": "19fc0dd0-0da7-4050-9ab6-8b7d05ed5ccd", "country_id": "b661bb73-...", "name": "Mobile Wallet (M-PESA)", "code": "M PESA", "channel_type": "phone", "status": "active", "synced_at": "..."}
]
```

## `GET /v1/channels`

Un "channel" represente une combinaison pays/devise/type/sens de paiement disponible. **C'est `channel_id` que vous devez fournir dans une requete de depot/retrait.** Filtres disponibles en query params : `country_id`, `channel_type`, `ramp_type` (`deposit` | `withdraw`).

```bash
curl "https://threewfpayment.onrender.com/v1/channels?ramp_type=deposit&channel_type=momo&country_id=b661bb73-fcbf-45cb-b317-79db87a1b3d2" \
  -H "Authorization: Bearer <token>"
```

```json
[
  {
    "id": "96ee8110-d1c2-4606-8d27-05c2aa6a4f98",
    "country_id": "b661bb73-fcbf-45cb-b317-79db87a1b3d2",
    "currency_code": "KES",
    "channel_type": "momo",
    "ramp_type": "deposit",
    "status": "active",
    "min_amount": "150.00",
    "max_amount": "250000.00",
    "synced_at": "2026-07-24T18:21:18Z"
  }
]
```

`channel_type` observes en pratique : `bank`, `momo`, `eft`, `p2p`, `spenn`, `virtualbank`, `phone` — ce n'est **pas** une liste figee, traitez-la comme informative plutot que comme un enum strict cote client. Respectez `min_amount`/`max_amount` (un `0.00` sur `max_amount` signifie generalement "pas de plafond documente", mais restez prudent et validez cote Yellow Card via un premier test en sandbox).

## `GET /v1/currencies`

```bash
curl "https://threewfpayment.onrender.com/v1/currencies" \
  -H "Authorization: Bearer <token>"
```

```json
[
  {"id": "007f5a39-cf79-461d-8386-81819ba3341b", "code": "BRL", "name": "Brazilian Real", "country_id": "8b02acac-...", "is_active": true}
]
```
