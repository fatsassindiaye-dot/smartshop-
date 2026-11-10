import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from boutique.models import Commande

def envoyer_commande(commande):
    url = settings.SMARTCUSTOMER_API_URL
    token = settings.SMARTCUSTOMER_API_TOKEN
    if not url or not token:
        return False
    if not url.startswith('https://') and not (settings.DEBUG and url.startswith('http://127.0.0.1:')):
        return False
    payload = {'commande_id':commande.pk,'nom':commande.nom,'email':commande.utilisateur.email or '', 'telephone':commande.telephone,'adresse':commande.adresse,'statut':commande.statut,'total':str(commande.total),'date_commande':commande.cree_le.isoformat(),'produits':[{'nom':ligne.nom_produit,'quantite':ligne.quantite,'prix_unitaire':str(ligne.prix_unitaire)} for ligne in commande.lignes.all()]}
    try:
        r = requests.post(url.rsplit('/evenements/',1)[0].rstrip('/')+'/commandes/', json=payload, headers={'Authorization':'Bearer '+token}, timeout=settings.SMARTCUSTOMER_TIMEOUT)
        r.raise_for_status()
        return True
    except requests.RequestException:
        return False

class Command(BaseCommand):
    help='Synchronise les commandes SmartShop vers SmartCustomer (idempotent, réexécutable).'
    def handle(self,*args,**kwargs):
        if not settings.SMARTCUSTOMER_API_URL or not settings.SMARTCUSTOMER_API_TOKEN:
            raise CommandError('Configurer SMARTCUSTOMER_API_URL et SMARTCUSTOMER_API_TOKEN')
        ok = 0
        for commande in Commande.objects.prefetch_related('lignes').select_related('utilisateur').order_by('pk'):
            if envoyer_commande(commande): ok += 1
            else: self.stderr.write(f'Commande #{commande.pk} non synchronisée')
        self.stdout.write(f'{ok} commande(s) acceptée(s) par SmartCustomer.')
