# Guide d'intégration — Payment Platform API

**Public visé :** développeurs des produits internes de l'entreprise (3WF, GeMTI-Cash, et futurs projets) qui doivent envoyer ou recevoir de l'argent via Yellow Card.

**Ce que c'est :** Payment Platform est la passerelle interne unique vers Yellow Card. Votre produit ne parle jamais directement à Yellow Card — il passe par cette API, qui gère l'authentification Yellow Card, la signature des requêtes, le mapping des statuts et le suivi des transactions.

**Ce que ce n'est pas :** un SDK ou une librairie front-end. C'est une API HTTP serveur-à-serveur — n'appelez jamais ces endpoints depuis du JavaScript exécuté dans un navigateur (voir [Sécurité](#sécurité)).

---

## 1. Sommaire

- [Démarrage rapide](#2-démarrage-rapide)
- [Obtenir un projet et une clé API](#3-obtenir-un-projet-et-une-clé-api)
- [Authentification](#4-authentification)
- [Données de référence](#5-données-de-référence-pays-réseaux-channels-devises)
- [Dépôts](#6-dépôts-deposits)
- [Retraits](#7-retraits-withdrawals)
- [Crypto sends (fonctionnalité en pause)](#8-crypto-sends-fonctionnalité-en-pause)
- [Cycle de vie et suivi des statuts](#9-cycle-de-vie-et-suivi-des-statuts)
- [Idempotence](#10-idempotence)
- [Gestion des erreurs](#11-gestion-des-erreurs)
- [Pagination](#12-pagination)
- [Limites, quotas, disponibilité](#13-limites-quotas-disponibilité)
- [Sécurité](#14-sécurité)
- [Documentation interactive](#15-documentation-interactive)
- [Support](#16-support)

---

## 2. Démarrage rapide

```bash
# 1. Échanger votre clé API contre un token d'accès (valable 15 minutes)
curl -X POST "$PAYMENT_PLATFORM_URL/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "pp_<prefix>_<secret>"}'

# -> {"access_token": "eyJ...", "token_type": "bearer", "expires_in": 900}

# 2. Utiliser le token pour appeler l'API
curl "$PAYMENT_PLATFORM_URL/v1/countries" \
  -H "Authorization: Bearer eyJ..."
```

`$PAYMENT_PLATFORM_URL` : URL de base de l'environnement de déploiement (à obtenir auprès de l'équipe plateforme — pas encore de domaine de production au moment de la rédaction de ce guide). En développement local, c'est `http://localhost:8000`.

---

## 3. Obtenir un projet et une clé API

Payment Platform organise les intégrations par **projet** (un projet = un produit consommateur, ex. "3WF", "GeMTI-Cash User App"). Chaque projet a :

- un **environnement** (`sandbox` ou `production`) qui détermine quelles credentials Yellow Card sont utilisées côté serveur — vous n'avez rien à configurer à ce sujet, c'est géré par la plateforme ;
- une ou plusieurs **clés API**, chacune avec des **scopes** (permissions).

**Comment obtenir les vôtres :** un administrateur `super_admin` doit créer votre projet et émettre une clé API depuis le dashboard admin (`/admins` et `/projects`). La clé complète (format `pp_<prefix>_<secret>`) n'est affichée **qu'une seule fois** à sa création — récupérez-la immédiatement et stockez-la dans votre gestionnaire de secrets (jamais dans le code, jamais commitée).

Scopes disponibles :

| Scope | Autorise |
|---|---|
| `deposits:write` | `POST /v1/deposits` |
| `withdrawals:write` | `POST /v1/withdrawals` |
| `transactions:read` | Tous les `GET` sur `/v1/deposits`, `/v1/withdrawals`, `/v1/crypto-sends`, `/v1/transactions` |
| `crypto_sends:write` | `POST /v1/crypto-sends` (non accordé par défaut — voir [§8](#8-crypto-sends-fonctionnalité-en-pause)) |

Par défaut, une nouvelle clé reçoit `deposits:write`, `withdrawals:write`, `transactions:read`. Si un scope vous manque, contactez un `super_admin` pour qu'il en émette une nouvelle avec les scopes voulus (une clé ne peut pas être modifiée après coup — il faut la faire tourner : révocation + nouvelle clé, via `/projects/api-keys/{id}/rotate` côté admin).

Si votre projet a besoin d'accéder à Yellow Card en environnement `production`, demandez explicitement cet environnement à la création du projet — un projet `sandbox` ne peut jamais toucher de l'argent réel.

---

## 4. Authentification

Payment Platform n'utilise **pas OAuth**. Le flux est :

1. Vous détenez une clé API complète (`pp_<prefix>_<secret>`), obtenue une seule fois à la création (§3).
2. Vous l'échangez contre un **token JWT court** via `POST /v1/auth/token`.
3. Vous utilisez ce token en `Authorization: Bearer <token>` sur tous les appels `/v1/*` suivants.
4. Le token expire au bout de **15 minutes** (`expires_in: 900`) — ré-échangez votre clé API pour en obtenir un nouveau. Ne cachez pas le token plus longtemps ; ré-échangez proactivement (ex. dès qu'il reste < 1 minute) plutôt que d'attendre un 401.

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

Un token invalide, mal formé ou expiré renvoie **401** sur n'importe quel endpoint `/v1/*` :

```json
{"detail": "Token invalide"}
```

Une clé API invalide ou révoquée renvoie **401** dès l'échange :

```json
{"detail": "Cle API invalide ou revoquee"}
```

---

## 5. Données de référence (pays, réseaux, channels, devises)

Avant de créer un dépôt ou un retrait, vous devez résoudre les identifiants Payment Platform (des UUID internes — **pas** les identifiants Yellow Card bruts) via ces endpoints. Ils sont synchronisés régulièrement depuis Yellow Card ; ne codez jamais un UUID en dur dans votre application, résolvez-le à chaque fois (ou cachez-le avec une expiration courte).

### `GET /v1/countries`

```json
[
  {"id": "b661bb73-fcbf-45cb-b317-79db87a1b3d2", "iso_code": "KE", "name": "Kenya", "is_active": true, "synced_at": "2026-07-24T18:23:01Z"}
]
```

### `GET /v1/networks`

Un "réseau" est une banque ou un opérateur mobile money précis (ex. M-PESA au Kenya).

```json
[
  {"id": "19fc0dd0-0da7-4050-9ab6-8b7d05ed5ccd", "country_id": "b661bb73-...", "name": "Mobile Wallet (M-PESA)", "code": "M PESA", "channel_type": "phone", "status": "active", "synced_at": "..."}
]
```

### `GET /v1/channels`

Un "channel" représente une combinaison pays/devise/type/sens de paiement disponible. **C'est `channel_id` que vous devez fournir dans une requête de dépôt/retrait.** Filtres disponibles en query params : `country_id`, `channel_type`, `ramp_type` (`deposit` | `withdraw`).

```
GET /v1/channels?ramp_type=deposit&channel_type=momo&country_id=b661bb73-fcbf-45cb-b317-79db87a1b3d2
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

`channel_type` observés en pratique : `bank`, `momo`, `eft`, `p2p`, `spenn`, `virtualbank`, `phone` — ce n'est **pas** une liste figée, traitez-la comme informative plutôt que comme un enum strict côté client. Respectez `min_amount`/`max_amount` (un `0.00` sur `max_amount` signifie généralement "pas de plafond documenté", mais restez prudent et validez côté Yellow Card via un premier test en sandbox).

### `GET /v1/currencies`

```json
[
  {"id": "007f5a39-cf79-461d-8386-81819ba3341b", "code": "BRL", "name": "Brazilian Real", "country_id": "8b02acac-...", "is_active": true}
]
```

Tous les endpoints `/v1/*` (y compris ceux-ci) nécessitent le header `Authorization: Bearer <token>` du §4.

---

## 6. Dépôts (`deposits`)

Un dépôt = un utilisateur final envoie de l'argent vers le wallet Yellow Card du produit (cash-in).

### `POST /v1/deposits` — scope `deposits:write`

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

Réponse `201` :

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

Champs clés :

| Champ | Description |
|---|---|
| `client_reference` | **Votre** clé d'idempotence (unique par projet). Rejouer le même appel avec la même valeur renvoie la transaction existante au lieu d'en créer une nouvelle — voir [§10](#10-idempotence). |
| `customer_uid` | Identifiant de l'utilisateur dans **votre** système (pas transmis tel quel à Yellow Card, sert à votre traçabilité). |
| `local_amount` | Montant en devise locale, **entier sans décimales** (Yellow Card l'exige). |
| `channel_id` / `source_network_id` | Résolus via `/v1/channels` et `/v1/networks` (§5) — jamais un ID Yellow Card brut. |
| `source_account_number` | Numéro de téléphone (momo) ou de compte (bank) du payeur. **Format international requis pour les numéros de téléphone** (ex. `+254712345678`, pas `254712345678` — Yellow Card rejette le format national, voir l'erreur type ci-dessous). |
| `recipient` | KYC minimal du titulaire du wallet destinataire. Les champs requis varient selon `customer_type` et le pays — en cas de doute, remplissez-les tous. |
| `force_accept` | Laissez `true` sauf besoin spécifique (évite un état intermédiaire "à confirmer manuellement" côté Yellow Card). |

Exemple d'erreur Yellow Card réelle rencontrée en sandbox (numéro sans indicatif international) :

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
→ HTTP `502`. Voir [§11](#11-gestion-des-erreurs).

### `GET /v1/deposits/{id}` et `GET /v1/deposits` — scope `transactions:read`

`GET /v1/deposits/{id}` déclenche automatiquement un rafraîchissement du statut auprès de Yellow Card si la transaction n'est pas encore dans un état terminal (voir [§9](#9-cycle-de-vie-et-suivi-des-statuts)) — c'est le mécanisme de secours en l'absence de webhook.

`GET /v1/deposits?status=completed&limit=50&offset=0` liste les dépôts du projet, filtrable par `status`.

---

## 7. Retraits (`withdrawals`)

Un retrait = le produit envoie de l'argent depuis le wallet Yellow Card vers un utilisateur final (cash-out). Même logique que les dépôts, avec `destination_*` au lieu de `source_*` et `sender` au lieu de `recipient`.

### `POST /v1/withdrawals` — scope `withdrawals:write`

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

Réponse `201` :

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

`reason` est **requis** pour un retrait (contrairement au dépôt où il a une valeur par défaut). `GET /v1/withdrawals/{id}` et `GET /v1/withdrawals` fonctionnent comme pour les dépôts.

---

## 8. Crypto sends (fonctionnalité en pause)

`POST /v1/crypto-sends` existe dans l'API (envoi depuis le solde Yellow Card vers une adresse crypto externe) mais **cette fonctionnalité est actuellement mise en pause côté produit** : le scope `crypto_sends:write` n'est accordé à aucun projet par défaut, et l'intégration Yellow Card sous-jacente n'a pas encore été validée de bout en bout en sandbox.

**Ne construisez pas d'intégration dépendant de cet endpoint sans en parler d'abord à l'équipe plateforme.** Si votre produit a besoin d'envoyer des paiements crypto, contactez l'équipe pour évaluer l'état d'avancement avant de démarrer.

---

## 9. Cycle de vie et suivi des statuts

Statuts possibles (champ `status` sur une transaction) :

| Statut | Sens |
|---|---|
| `pending` | Créée, pas encore traitée par Yellow Card. |
| `processing` | En cours de traitement. |
| `completed` | **Terminal.** Fonds arrivés. |
| `failed` | **Terminal.** Échec (voir `failure_reason` si présent). |
| `cancelled` | **Terminal.** Annulée. |
| `expired` | **Terminal.** Expirée avant complétion. |

**Il n'y a actuellement aucun webhook sortant depuis Payment Platform vers les projets consommateurs.** Payment Platform reçoit lui-même les webhooks de Yellow Card et les applique en interne, mais ne les retransmet pas encore à votre produit. Pour suivre l'évolution d'une transaction, vous devez **poller** :

- `GET /v1/{deposits|withdrawals|crypto-sends|transactions}/{id}` rafraîchit activement le statut auprès de Yellow Card si la transaction n'est pas dans un état terminal (l'appel peut donc être légèrement plus lent qu'un simple GET tant que le statut n'est pas final).
- Une fois `status` dans un état terminal, il ne changera plus — vous pouvez arrêter de poller.
- Fréquence recommandée : quelques secondes à quelques dizaines de secondes après création, avec backoff progressif si l'état reste `pending`/`processing` longtemps.

Si votre produit a besoin de notifications push (webhook sortant) plutôt que du polling, remontez ce besoin à l'équipe plateforme — ce n'est pas encore construit.

---

## 10. Idempotence

`client_reference` est votre clé d'idempotence, **unique par projet** (deux projets différents peuvent réutiliser la même valeur sans collision). Si vous rejouez un `POST /v1/deposits` ou `POST /v1/withdrawals` avec un `client_reference` déjà vu, Payment Platform renvoie la transaction existante (même code `201`, pas d'erreur, pas de nouvelle transaction créée) au lieu de re-soumettre la requête à Yellow Card. Utilisez systématiquement un identifiant stable généré une seule fois par intention de paiement côté client (pas un timestamp ou un UUID regénéré à chaque retry).

---

## 11. Gestion des erreurs

| Code | Cas | Corps |
|---|---|---|
| `401` | Token manquant, invalide ou expiré | `{"detail": "Token invalide"}` ou `{"detail": "Token manquant"}` |
| `401` | Clé API invalide/révoquée (sur `/v1/auth/token`) | `{"detail": "Cle API invalide ou revoquee"}` |
| `403` | Scope manquant sur le token | `{"detail": "Scope manquant : 'crypto_sends:write'"}` |
| `404` | Transaction introuvable ou n'appartenant pas à votre projet | `{"detail": "Transaction introuvable"}` |
| `422` | Corps de requête invalide (champ manquant/mal typé) | `{"detail": [{"type": "missing", "loc": ["body", "customer_uid"], "msg": "Field required", ...}, ...]}` (format standard FastAPI/Pydantic — une entrée par champ en erreur) |
| `422` | `channel_id`/`network_id` non résolu | `{"detail": "..."}` |
| `502` | Yellow Card a rejeté la requête | `{"detail": {"message": "Yellow Card a rejete la requete de depot", "yellowcard_error": {"code": "...", "message": "..."}}}` — inspectez `yellowcard_error` pour la cause exacte (ex. format de téléphone, montant hors plage, channel indisponible). |

Sur un `502`, la transaction **n'a pas été créée côté Payment Platform** — vous pouvez corriger et retenter avec le même `client_reference` sans risque de doublon.

---

## 12. Pagination

Les endpoints de liste (`GET /v1/deposits`, `/v1/withdrawals`, `/v1/crypto-sends`, `/v1/transactions`) acceptent `limit` (défaut 50, max 200) et `offset` (défaut 0). Il n'y a pas de curseur ni de total count dans la réponse — utilisez `limit`/`offset` classiques et arrêtez de paginer quand une page revient plus courte que `limit`.

---

## 13. Limites, quotas, disponibilité

- Aucune limite de débit (rate limiting) n'est actuellement appliquée par Payment Platform. Restez raisonnable dans le volume d'appels — une limite pourra être introduite plus tard sans préavis si nécessaire.
- Aucun SLA formel n'existe à ce stade (produit interne early-stage). En cas d'incident, contactez l'équipe plateforme (§16).
- `GET /health` et `GET /health/ready` (hors `/v1`) exposent l'état de santé de l'API pour vos propres checks amont si besoin.

---

## 14. Sécurité

- **Ne jamais** appeler ces endpoints depuis du code exécuté côté navigateur/mobile client — l'API n'autorise pas les origines CORS publiques (seul le dashboard admin est autorisé). Toute intégration doit se faire depuis votre backend.
- La clé API complète n'est affichée **qu'une fois** à sa création/rotation. Si elle est perdue, elle ne peut pas être récupérée — il faut la faire tourner (rotation) via un admin.
- Stockez la clé API dans votre gestionnaire de secrets (jamais en dur dans le code, jamais dans un dépôt Git, jamais dans des logs).
- En cas de fuite suspectée d'une clé, contactez immédiatement un `super_admin` pour la révoquer (`/projects/api-keys/{id}/revoke` côté admin) et en émettre une nouvelle.
- Les tokens JWT de courte durée (§4) limitent la fenêtre d'exposition en cas de fuite d'un token — ne les journalisez pas.

---

## 15. Documentation interactive

L'API expose une documentation OpenAPI auto-générée et toujours synchronisée avec le code déployé :

- Swagger UI : `$PAYMENT_PLATFORM_URL/docs`
- ReDoc : `$PAYMENT_PLATFORM_URL/redoc`
- Schéma brut : `$PAYMENT_PLATFORM_URL/openapi.json`

Utile pour explorer les schémas exacts (types, champs optionnels) sans dépendre de ce guide si un doute persiste.

---

## 16. Support

- **Obtenir un projet / une clé API / changer des scopes :** demander à un administrateur `super_admin` du dashboard Payment Platform (section "Administrateurs" / "Projets & clés API").
- **Question sur un cas d'erreur, une intégration bloquée, un besoin non couvert par ce guide (webhooks sortants, crypto sends, nouveau pays/devise) :** contacter l'équipe plateforme directement.
- **Suivi des transactions en production :** le dashboard admin (Monitoring, Journal d'audit, Webhooks) permet à l'équipe plateforme d'investiguer un incident sur une transaction précise — donnez la `reference` ou l'`id` de la transaction concernée.
