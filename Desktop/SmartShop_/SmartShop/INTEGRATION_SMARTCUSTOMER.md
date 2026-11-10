# Intégration SmartCustomer — contrat API proposé

Le dashboard existant : https://smartcustomer-analytics.onrender.com/dashboard/ . Cette page n'est **pas** une API. Sans les fichiers `main/models.py`, `main/views.py`, `main/urls.py` et `settings.py` du projet SmartCustomer, impossible de garantir la compatibilité. Ne remplacez pas son code par ce ZIP.

## Contrat de réception à implémenter côté SmartCustomer

- `POST /api/smartshop/evenements/`
- En-tête : `Authorization: Bearer <jeton-secret-partagé>`
- JSON :

```json
{
  "event_id": "4b66f14a-9445-4c1a-8cb8-079d74ab33ab",
  "session_id": "session-django",
  "user_id": 2,
  "type_evenement": "product_view",
  "page": "/produit/1/",
  "produit_id": 1,
  "commande_id": null,
  "valeur": null,
  "date_evenement": "2026-10-29T12:00:00+00:00"
}
```

Le récepteur doit : vérifier le jeton côté serveur en temps constant, valider les champs et les types, vérifier la taille maximale du JSON, refuser les événements inconnus, dédupliquer sur `event_id`, enregistrer l'événement et répondre avec un code HTTP 2xx **uniquement si l'enregistrement a réussi**. Éviter de créer un nouveau client SmartCustomer pour chaque page vue ; agréger les sessions et événements selon la logique métier de votre application. Prévoir une table d'événements dédiée et des migrations. Ne jamais accepter une URL de retour ou un identifiant client sans vérification. Préférer HTTPS, limiter le débit et journaliser les erreurs sans exposer de secrets.

## Mise en route

Après création et déploiement de l'endpoint dans SmartCustomer :

```env
SMARTCUSTOMER_API_URL=https://smartcustomer-analytics.onrender.com/api/smartshop/evenements/
SMARTCUSTOMER_API_TOKEN=UN_LONG_JETON_ALEATOIRE_IDENTIQUE_COTE_RECEPTEUR
```

**Cette URL est un exemple de route à créer : elle n'existe pas nécessairement aujourd'hui.**

Dans SmartShop :

```cmd
python manage.py envoyer_evenements
```

Les événements réussis passent à `transmis=True` ; les échecs sont conservés pour réessai. Une API distante qui répond 2xx mais n'enregistre pas réellement les données est une mauvaise intégration.

## Champs disponibles pour les indicateurs

- `page_view` : nombre de pages vues, visites à agréger par `session_id`.
- `product_view` : produits consultés, produits populaires.
- `add_to_cart` / `remove_from_cart` / `cart_update` : interactions avec le panier.
- `purchase` : commande **simulée** et montant.

**Non encore inclus :** mesure fiable du temps actif, clics génériques, paiement réel, modèle IA entraîné sur ces données. Ne présentez pas ces métriques comme disponibles sans les implémenter et les valider.
