**Public vise :** developpeurs des produits internes de l'entreprise (3WF, GeMTI-Cash, et futurs projets) qui doivent envoyer ou recevoir de l'argent via Yellow Card.

**Ce que c'est :** Payment Platform est la passerelle interne unique vers Yellow Card. Votre produit ne parle jamais directement a Yellow Card — il passe par cette API, qui gere l'authentification Yellow Card, la signature des requetes, le mapping des statuts et le suivi des transactions.

**Ce que ce n'est pas :** un SDK ou une librairie front-end. C'est une API HTTP serveur-a-serveur — n'appelez jamais ces endpoints depuis du JavaScript execute dans un navigateur (voir [Securite & limites](/docs/security)).

## URL de base

| Environnement | URL |
|---|---|
| **Production** | `https://threewfpayment.onrender.com` |
| Developpement local | `http://localhost:8000` |

Tous les exemples de ce guide utilisent l'URL de production. Tous les endpoints d'integration vivent sous le prefixe `/v1` (ex. `https://threewfpayment.onrender.com/v1/deposits`) — c'est un prefixe de version d'API, pas un dossier de documentation.

## Demarrage rapide

```bash
# 1. Echanger votre cle API contre un token d'acces (valable 15 minutes)
curl -X POST "https://threewfpayment.onrender.com/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"api_key": "pp_<prefix>_<secret>"}'

# -> {"access_token": "eyJ...", "token_type": "bearer", "expires_in": 900}

# 2. Utiliser le token pour appeler l'API
curl "https://threewfpayment.onrender.com/v1/countries" \
  -H "Authorization: Bearer eyJ..."
```

## Par ou commencer ?

1. **[Obtenir un projet et une cle API](/docs/getting-started)** — la premiere chose a faire avant tout appel.
2. **[Authentification](/docs/authentication)** — comprendre l'echange cle → token.
3. **[Donnees de reference](/docs/reference-data)** — resoudre les identifiants pays/reseaux/channels necessaires aux depots et retraits.
4. **[Depots](/docs/deposits)** et **[Retraits](/docs/withdrawals)** — les deux operations principales.
5. **[Statuts & suivi des transactions](/docs/transactions)** — comment savoir qu'un paiement est arrive.
