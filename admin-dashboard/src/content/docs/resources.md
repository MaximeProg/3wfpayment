## Documentation interactive

L'API expose une documentation OpenAPI auto-generee et toujours synchronisee avec le code deploye :

- Swagger UI : [https://threewfpayment.onrender.com/docs](https://threewfpayment.onrender.com/docs)
- ReDoc : [https://threewfpayment.onrender.com/redoc](https://threewfpayment.onrender.com/redoc)
- Schema brut : [https://threewfpayment.onrender.com/openapi.json](https://threewfpayment.onrender.com/openapi.json)

Utile pour explorer les schemas exacts (types, champs optionnels) sans dependre de ce guide si un doute persiste.

## Support

- **Obtenir un projet / une cle API / changer des scopes :** demander a un administrateur `super_admin` du dashboard Payment Platform (section *Administrateurs* / *Projets & cles API*).
- **Question sur un cas d'erreur, une integration bloquee, un besoin non couvert par ce guide (webhooks sortants, crypto sends, nouveau pays/devise) :** contacter l'equipe plateforme directement.
- **Suivi des transactions en production :** le dashboard admin (Monitoring, Journal d'audit, Webhooks) permet a l'equipe plateforme d'investiguer un incident sur une transaction precise — donnez la `reference` ou l'`id` de la transaction concernee.
