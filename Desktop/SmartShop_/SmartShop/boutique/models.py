from django.conf import settings
from django.db import models

class Produit(models.Model):
    CATEGORIES=[('telephone','Téléphones'),('vetement','Vêtements'),('chaussure','Chaussures'),('cosmetique','Cosmétiques'),('accessoire','Accessoires'),('maison','Maison')]
    nom=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    prix=models.DecimalField(max_digits=12,decimal_places=0)
    categorie=models.CharField(max_length=30,choices=CATEGORIES)
    image=models.ImageField(upload_to='produits/',blank=True,null=True)
    stock=models.PositiveIntegerField(default=0)
    actif=models.BooleanField(default=True)
    date_creation=models.DateTimeField(auto_now_add=True)
    @property
    def image_demo_url(self):
        """Vraies photos studio nettes, propres et vibrantes (Unsplash HQ)."""
        photos = {
            'Samsung Galaxy A15': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=800&q=80',
            'iPhone 13': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?auto=format&fit=crop&w=800&q=80',
            'Robe élégante': 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=80',
            'Ensemble homme': 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80',
            'Baskets sport': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80',
            'Sac à main': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=800&q=80',
            'Parfum doux': 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=800&q=80',
            'Montre connectée': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80',
            'Lampe de bureau': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80',
            'Casque Bluetooth': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80',
            'Chaussures ville': 'https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?auto=format&fit=crop&w=800&q=80',
            'Chemise coton': 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80',
        }
        if self.nom in photos:
            return photos[self.nom]

        # Photos génériques par catégorie
        categories_photos = {
            'telephone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80',
            'vetement': 'https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?auto=format&fit=crop&w=800&q=80',
            'chaussure': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=800&q=80',
            'cosmetique': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=800&q=80',
            'accessoire': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80',
            'maison': 'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80',
        }
        if self.categorie in categories_photos:
            return categories_photos[self.categorie]

        from django.templatetags.static import static
        return static('images/produits/produit_01.jpg')

    def __str__(self): return self.nom

class Commande(models.Model):
    STATUTS=[('simulation','Simulation confirmée'),('annulee','Annulée')]
    utilisateur=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='commandes')
    nom=models.CharField(max_length=150)
    telephone=models.CharField(max_length=30)
    adresse=models.TextField()
    statut=models.CharField(max_length=20,choices=STATUTS,default='simulation')
    total=models.DecimalField(max_digits=12,decimal_places=0)
    cree_le=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Commande #{self.pk}'

class LigneCommande(models.Model):
    commande=models.ForeignKey(Commande,on_delete=models.CASCADE,related_name='lignes')
    produit=models.ForeignKey(Produit,on_delete=models.PROTECT)
    nom_produit=models.CharField(max_length=200)
    quantite=models.PositiveIntegerField()
    prix_unitaire=models.DecimalField(max_digits=12,decimal_places=0)
    def sous_total(self): return self.prix_unitaire*self.quantite
