# SmartShop — boutique Django prête pour VS Code

## Démarrage Windows CMD

1. Extraire le dossier `SmartShop` sur le Bureau. Ouvrir ce dossier dans VS Code.
2. Dans CMD :

```cmd
cd /d "%USERPROFILE%\Desktop\SmartShop"
python -m venv env
env\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py produits_demo
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

3. Visiter `http://127.0.0.1:8000/` ; administration `http://127.0.0.1:8000/admin/`.
4. Si les produits ne s'affichent pas, vérifier que `python manage.py produits_demo` a bien été exécutée.

## Fonctionnalités

Accueil, catalogue, recherche, filtres, fiches produits, panier en session, inscription, connexion, historique des commandes, validation de commande simulée, gestion du stock, administration, collecte des événements sous consentement, export vers une API SmartCustomer configurée.

**Images :** 12 illustrations de produits sont incluses localement dans `static/images/produits/` : elles fonctionnent sans Internet. Elles ne sont **pas des photographies**. Pour obtenir de vraies photos, ajouter des images depuis l'administration Django dans chaque fiche produit.

**Paiement :** simulation uniquement, aucun paiement réel.

**SmartCustomer :** le module émetteur existe, mais le projet SmartCustomer distant doit exposer une API réceptrice compatible, authentifiée, idempotente. Sans cette API et sans jeton, il n'y a pas de liaison réelle. Voir `INTEGRATION_SMARTCUSTOMER.md`.

**Production :** configuration de base destinée au développement. Prévoir une base persistante, stockage média, variables secrètes, déploiement sécurisé et validation complète avant mise en ligne.

## Tests

```cmd
python manage.py test
```

