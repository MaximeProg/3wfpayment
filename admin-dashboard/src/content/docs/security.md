## Limites, quotas, disponibilite

- Aucune limite de debit (rate limiting) n'est actuellement appliquee par Payment Platform. Restez raisonnable dans le volume d'appels — une limite pourra etre introduite plus tard sans preavis si necessaire.
- Aucun SLA formel n'existe a ce stade (produit interne early-stage). En cas d'incident, contactez [l'equipe plateforme](/docs/resources).
- `GET /health` et `GET /health/ready` (hors `/v1`) exposent l'etat de sante de l'API pour vos propres checks amont si besoin.

## Securite

- **Ne jamais** appeler ces endpoints depuis du code execute cote navigateur/mobile client — l'API n'autorise pas les origines CORS publiques (seul le dashboard admin est autorise). Toute integration doit se faire depuis votre backend.
- La cle API complete n'est affichee **qu'une fois** a sa creation/rotation. Si elle est perdue, elle ne peut pas etre recuperee — il faut la faire tourner (rotation) via un admin.
- Stockez la cle API dans votre gestionnaire de secrets (jamais en dur dans le code, jamais dans un depot Git, jamais dans des logs).
- En cas de fuite suspectee d'une cle, contactez immediatement un `super_admin` pour la revoquer et en emettre une nouvelle.
- Les tokens JWT de courte duree ([voir Authentification](/docs/authentication)) limitent la fenetre d'exposition en cas de fuite d'un token — ne les journalisez pas.
