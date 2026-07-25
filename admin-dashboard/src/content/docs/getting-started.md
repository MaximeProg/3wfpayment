Payment Platform organise les integrations par **projet** (un projet = un produit consommateur, ex. "3WF", "GeMTI-Cash User App"). Chaque projet a :

- un **environnement** (`sandbox` ou `production`) qui determine quelles credentials Yellow Card sont utilisees cote serveur — vous n'avez rien a configurer a ce sujet, c'est gere par la plateforme ;
- une ou plusieurs **cles API**, chacune avec des **scopes** (permissions).

## Comment obtenir les votres

Un administrateur `super_admin` doit creer votre projet et emettre une cle API depuis le dashboard admin (sections *Administrateurs* et *Projets & cles API*). La cle complete (format `pp_<prefix>_<secret>`) n'est affichee **qu'une seule fois** a sa creation — recuperez-la immediatement et stockez-la dans votre gestionnaire de secrets (jamais dans le code, jamais commitee).

## Scopes disponibles

| Scope | Autorise |
|---|---|
| `deposits:write` | `POST /v1/deposits` |
| `withdrawals:write` | `POST /v1/withdrawals` |
| `transactions:read` | Tous les `GET` sur `/v1/deposits`, `/v1/withdrawals`, `/v1/crypto-sends`, `/v1/transactions` |
| `crypto_sends:write` | `POST /v1/crypto-sends` (non accorde par defaut — voir [Crypto sends](/docs/crypto-sends)) |

Par defaut, une nouvelle cle recoit `deposits:write`, `withdrawals:write`, `transactions:read`. Si un scope vous manque, contactez un `super_admin` pour qu'il en emette une nouvelle avec les scopes voulus — une cle ne peut pas etre modifiee apres coup, il faut la faire tourner (revocation + nouvelle cle, via rotation cote admin).

Si votre projet a besoin d'acceder a Yellow Card en environnement `production`, demandez explicitement cet environnement a la creation du projet — un projet `sandbox` ne peut jamais toucher de l'argent reel.
