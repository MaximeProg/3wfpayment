# Cahier des charges — Payment Platform

| | |
|---|---|
| **Projet** | Payment Platform (nom provisoire) |
| **Version** | 1.0 |
| **Date** | 2026-07-24 |
| **Statut** | Draft — pour validation |
| **Fournisseur de paiement** | Yellow Card (Sandbox → Production) |

---

## 1. Contexte

L'entreprise exploite plusieurs produits nécessitant des fonctionnalités de paiement (dépôt, retrait, encaissement) :

- **3WF** — plateforme d'investissement (dépôts, retraits, opérations financières).
- **GeMTI-Cash** — portefeuille électronique, composé d'une application utilisateur et d'une application marchand.
- **Futurs projets** — non identifiés à ce jour, mais dont le besoin en paiement est acquis.

Yellow Card a été retenu comme partenaire de paiement unique. Un compte Sandbox est déjà disponible.

Intégrer Yellow Card séparément dans chaque produit dupliquerait le code, la logique métier, la gestion des erreurs et des webhooks, et multiplierait le coût de maintenance et la surface de risque (sécurité, conformité, régressions).

## 2. Objectif du projet

Construire une **plateforme de paiement interne unique** (« Payment Platform ») qui centralise toute intégration avec Yellow Card et expose une **API interne unifiée** à tous les produits de l'entreprise.

**Principe non négociable :** aucune application métier ne communique directement avec l'API Yellow Card. Toute communication transite exclusivement par la Payment Platform.

```
   3WF        GeMTI-Cash        Futurs projets
    │              │                   │
    └──────────────┼───────────────────┘
                    ▼
         ==========================
              Payment Platform
         ==========================
                    ▼
              Yellow Card API
```

## 3. Périmètre

### 3.1 Inclus dans le périmètre

- Une API backend exposant les opérations de paiement (dépôts, retraits, consultation, référentiels pays/réseaux/devises).
- La gestion complète de l'authentification Yellow Card (signature HMAC par requête, gestion et rotation des identifiants).
- La réception, la vérification et le traitement des webhooks Yellow Card.
- Un dashboard d'administration pour la supervision (transactions, projets, webhooks, monitoring).
- La gestion des projets clients internes (3WF, GeMTI-Cash, futurs projets) et de leurs clés d'API.
- La journalisation technique et fonctionnelle (logs, erreurs, audit).
- Une base de données propre et indépendante, hébergée sur **Neon** (PostgreSQL serverless).

### 3.2 Explicitement hors périmètre

- **Aucune gestion multi-provider.** La plateforme est conçue exclusivement autour de Yellow Card. Aucune abstraction, interface ou couche d'adaptation destinée à accueillir un futur fournisseur de paiement ne doit être développée à ce stade.
- La logique métier propre à chaque produit (règles d'investissement de 3WF, logique de portefeuille de GeMTI-Cash, etc.) reste dans les applications clientes.
- La gestion des utilisateurs finaux de 3WF ou GeMTI-Cash (comptes, KYC applicatif, etc.) n'est pas portée par la Payment Platform, sauf les données strictement nécessaires à l'exécution d'une transaction Yellow Card.

## 4. Acteurs

| Acteur | Description |
|---|---|
| **Application cliente (« projet »)** | Un produit interne consommateur de l'API (3WF, GeMTI-Cash, futur projet). Identifié par un enregistrement « Project » et authentifié par clé API. |
| **Administrateur plateforme** | Utilisateur du dashboard, supervise transactions, projets, webhooks et monitoring. |
| **Yellow Card** | Fournisseur de paiement externe (API + webhooks). |
| **Système (jobs internes)** | Processus automatisés : synchronisation des référentiels, traitement asynchrone des webhooks. |

## 5. Exigences fonctionnelles

### 5.1 Authentification Yellow Card

> Précision technique (validée par les docs officielles Yellow Card durant l'implémentation) : l'API Yellow Card ne fonctionne pas par jeton OAuth avec expiration, mais par **signature HMAC-SHA256 de chaque requête** (schéma `YcHmacV1`, clé API + secret). Il n'y a donc pas de « renouvellement de token » à proprement parler ; les exigences ci-dessous portent sur la gestion des identifiants (clé/secret) utilisés pour signer.

- FE-01 : Le système signe chaque appel sortant vers Yellow Card avec les identifiants (clé API + secret) de l'environnement concerné (Sandbox/Production).
- FE-02 : Les identifiants Yellow Card sont gérés de façon centralisée et peuvent être remplacés (rotation) sans redéploiement applicatif.
- FE-03 : Les identifiants d'accès à Yellow Card (clé API, secret) sont stockés de manière chiffrée.
- FE-04 : Toute défaillance d'authentification (signature rejetée, identifiants invalides) est journalisée et remonte une alerte exploitable dans le dashboard.

### 5.2 Référentiels (pays, réseaux, devises, méthodes de paiement)

- FE-05 : Synchronisation périodique des pays, réseaux Mobile Money, méthodes de paiement et devises supportées par Yellow Card.
- FE-06 : Ces référentiels sont mis en cache localement (base de données + cache applicatif) pour éviter les appels redondants à Yellow Card.
- FE-07 : Les applications clientes peuvent consulter ces référentiels via l'API interne.
- FE-08 : Une synchronisation manuelle peut être déclenchée depuis le dashboard.

### 5.3 Dépôts

- FE-09 : Une application cliente peut initier un dépôt via l'API interne.
- FE-10 : L'application cliente peut suivre le statut d'un dépôt en cours.
- FE-11 : Le résultat final (succès, échec, expiration) est accessible via l'API et notifiable à l'application cliente.

### 5.4 Retraits

- FE-12 : Une application cliente peut créer une demande de retrait.
- FE-13 : Le retrait peut être suivi jusqu'à son exécution complète.
- FE-14 : Le statut final du retrait est disponible via l'API.

### 5.5 Consultation des transactions

- FE-15 : Recherche et filtrage des transactions (par projet, statut, type, période, devise, pays, référence).
- FE-16 : Historique complet et détail d'une transaction, incluant les données brutes retournées par Yellow Card.
- FE-17 : Statut consultable en temps quasi réel (mise à jour via webhook ou polling de secours).

### 5.6 Webhooks

- FE-18 : La plateforme est le seul point de réception des webhooks Yellow Card ; aucune application cliente ne reçoit de webhook Yellow Card directement.
- FE-19 : Chaque webhook reçu est authentifié (vérification de signature/origine) avant traitement.
- FE-20 : Les événements sont enregistrés (payload brut conservé) même en cas d'échec de traitement.
- FE-21 : Le traitement d'un webhook met à jour le statut de la transaction concernée et déclenche, si nécessaire, une notification vers l'application cliente d'origine.
- FE-22 : Le traitement est idempotent (un même événement reçu plusieurs fois ne produit pas d'effets de bord dupliqués).

### 5.7 Gestion des erreurs et journalisation

- FE-23 : Toute erreur (API Yellow Card, réseau, métier, synchronisation) est centralisée dans un journal technique consultable.
- FE-24 : Les erreurs sont catégorisées par source et par sévérité.
- FE-25 : Les actions administratives sensibles sont tracées dans un journal d'audit distinct.

### 5.8 Gestion des projets clients

- FE-26 : Un administrateur peut créer, activer, désactiver un projet client.
- FE-27 : Un administrateur peut générer une clé API pour un projet, effectuer une rotation de clé, et consulter l'historique d'activité du projet.
- FE-28 : Chaque transaction est systématiquement rattachée à son projet d'origine.

### 5.9 Dashboard d'administration

- FE-29 : Tableau de bord synthétique (volume traité, nombre de transactions par statut, activité par projet).
- FE-30 : Liste, recherche, filtre et détail des transactions, avec historique des changements de statut.
- FE-31 : Gestion des projets et des clés API.
- FE-32 : Visualisation des webhooks reçus, de leur statut de traitement et des erreurs associées.
- FE-33 : Écran de monitoring : disponibilité de Yellow Card, erreurs récentes, indicateurs de performance.

## 6. Exigences non fonctionnelles

| Réf | Exigence |
|---|---|
| NFE-01 | **Sécurité** : authentification forte des administrateurs, clé API distincte par projet, chiffrement des secrets au repos, endpoints sensibles protégés, TLS obligatoire de bout en bout. |
| NFE-02 | **Auditabilité** : toute action administrative (création/désactivation de projet, rotation de clé, modification de paramètre) est journalisée avec auteur, date et contexte. |
| NFE-03 | **Fiabilité** : aucune perte de transaction ; en cas d'échec de traitement d'un webhook, l'événement reste disponible pour rejouer le traitement. |
| NFE-04 | **Traçabilité** : chaque transaction conserve l'historique complet de ses changements de statut et les réponses brutes de Yellow Card. |
| NFE-05 | **Performance** : les référentiels (pays/réseaux/devises) sont servis depuis le cache local, sans appel systématique à Yellow Card. |
| NFE-06 | **Disponibilité** : la plateforme doit rester opérationnelle indépendamment des indisponibilités ponctuelles de Yellow Card (dégradation contrôlée, pas de panne en cascade). |
| NFE-07 | **Évolutivité** : la plateforme doit pouvoir accueillir de nouveaux projets clients sans modification de son cœur métier ni nouvelle intégration Yellow Card. |
| NFE-08 | **Maintenabilité** : une seule base de code, une documentation technique unique et à jour (OpenAPI/Swagger), pensée pour un usage pluriannuel. |
| NFE-09 | **Isolation des données** : les données d'un projet ne sont jamais visibles ou accessibles par un autre projet via l'API. |

## 7. Contraintes

- Stack technique imposée, alignée sur l'existant de l'entreprise : FastAPI, SQLAlchemy, PostgreSQL, Redis, Next.js/React/TypeScript.
- Base de données hébergée sur **Neon** (PostgreSQL serverless).
- Fournisseur de paiement unique : **Yellow Card**. Pas de conception multi-provider.
- Démarrage des développements et tests sur l'environnement **Sandbox** Yellow Card existant ; bascule en production ultérieure.
- La plateforme doit être conçue comme un **produit interne autonome**, avec son propre cycle de vie, indépendant des roadmaps de 3WF et GeMTI-Cash.

## 8. Entités principales du système (vue métier)

Projects · API Keys · Transactions · Deposits · Withdrawals · Webhooks · Countries · Networks · Currencies · Audit Logs · Error Logs · System Settings.

(Le détail technique — colonnes, types, relations — est spécifié dans le [Plan technique](./plan-technique.md).)

## 9. Livrables attendus

1. API backend (FastAPI) documentée (OpenAPI/Swagger), déployable, couvrant l'ensemble des exigences fonctionnelles ci-dessus.
2. Dashboard d'administration (Next.js) couvrant les écrans décrits en section 5.9.
3. Base de données Neon provisionnée, avec migrations versionnées.
4. Documentation technique unique (architecture, guide d'intégration pour les équipes produit, guide d'exploitation).
5. Environnement Sandbox opérationnel de bout en bout (dépôt, retrait, webhook) avant toute intégration avec 3WF ou GeMTI-Cash.

## 10. Critères d'acceptation (Definition of Done du MVP)

- [ ] Un projet peut être créé dans le dashboard et obtient une clé API fonctionnelle.
- [ ] Ce projet peut, via l'API interne, lister les pays/réseaux/devises disponibles.
- [ ] Ce projet peut initier un dépôt Sandbox et en suivre le statut jusqu'à son terme via webhook.
- [ ] Ce projet peut initier un retrait Sandbox et en suivre le statut jusqu'à son terme via webhook.
- [ ] Toute transaction est visible, avec son historique complet, dans le dashboard.
- [ ] Tout webhook reçu est visible dans le dashboard, avec son statut de traitement.
- [ ] Le renouvellement du token Yellow Card est automatique et ne nécessite aucune intervention manuelle sur une période d'observation d'au moins 7 jours.
- [ ] Aucune application cliente ne détient ou n'utilise de credentials Yellow Card.

## 11. Glossaire

| Terme | Définition |
|---|---|
| **Projet (Project)** | Application interne consommatrice de l'API Payment Platform (ex. 3WF). |
| **Transaction** | Terme générique désignant un dépôt ou un retrait. |
| **Webhook** | Notification asynchrone envoyée par Yellow Card à la Payment Platform pour signaler un changement d'état. |
| **Sandbox** | Environnement de test fourni par Yellow Card, sans mouvement d'argent réel. |
| **Rotation de clé** | Remplacement d'une clé API d'un projet par une nouvelle, invalidant l'ancienne. |
