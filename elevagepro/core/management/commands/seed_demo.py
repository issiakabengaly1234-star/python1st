from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from animals.models import Animal, Espece, MouvementAnimal, Naissance
from farms.models import Ferme
from health.models import Traitement, Vaccination
from transactions.models import Achat, Depense, PerteAnimal, VenteAnimal


class Command(BaseCommand):
    help = "Crée un compte de démonstration (demo / demo12345) avec des données d'exemple."

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(username="demo").exists():
            self.stdout.write("Le compte « demo » existe déjà : rien à faire.")
            return
        today = timezone.localdate()
        d = lambda days: today - timedelta(days=days)  # noqa: E731

        user = User.objects.create_user("demo", password="demo12345", first_name="Aminata", last_name="Traoré")
        eleveur = user.eleveur
        eleveur.telephone, eleveur.localisation = "+223 70 00 00 00", "Ségou"
        eleveur.save()

        ferme = Ferme.objects.create(nom="Ferme de la Plaine", proprietaire=eleveur, localisation="Ségou")
        ferme2 = Ferme.objects.create(nom="Bergerie du Fleuve", proprietaire=eleveur, localisation="Markala")

        bovin, _ = Espece.objects.get_or_create(nom="Bovin", defaults={"description": "Zébus et taurins"})
        ovin, _ = Espece.objects.get_or_create(nom="Ovin", defaults={"description": "Moutons"})
        caprin, _ = Espece.objects.get_or_create(nom="Caprin", defaults={"description": "Chèvres"})
        Espece.objects.get_or_create(nom="Volaille", defaults={"description": "Poules et pintades"})

        vache = Animal.objects.create(nom="Diama", sexe="F", espece=bovin, ferme=ferme, date_naissance=d(1500))
        Animal.objects.create(nom="Taureau", sexe="M", espece=bovin, ferme=ferme, date_naissance=d(1800))
        veau = Animal.objects.create(nom="Petit", sexe="M", espece=bovin, ferme=ferme, date_naissance=d(120), mere=vache)
        brebis = Animal.objects.create(nom="Neige", sexe="F", espece=ovin, ferme=ferme2, date_naissance=d(900))
        belier = Animal.objects.create(sexe="M", espece=ovin, ferme=ferme2, date_naissance=d(700))
        chevre = Animal.objects.create(nom="Biche", sexe="F", espece=caprin, ferme=ferme2, date_naissance=d(600))
        achete = Animal.objects.create(sexe="F", espece=caprin, ferme=ferme2, date_naissance=d(400))
        malade = Animal.objects.create(sexe="M", espece=ovin, ferme=ferme2, date_naissance=d(300))

        Naissance.objects.create(mere=vache, date=d(120), nombre=1, observations="Naissance sans complication")
        Naissance.objects.create(mere=brebis, date=d(40), nombre=2)
        Achat.objects.create(animal=achete, vendeur="Marché de Ségou", prix=45000, date=d(380))
        MouvementAnimal.objects.create(animal=achete, type="entree", date=d(380), origine="Marché de Ségou", destination=ferme2.nom)
        MouvementAnimal.objects.create(animal=belier, type="transfert", date=d(60), origine=ferme.nom, destination=ferme2.nom)

        Vaccination.objects.create(animal=vache, produit="Péripneumonie contagieuse bovine", date=d(340), prochaine_date=d(10))
        Vaccination.objects.create(animal=veau, produit="Charbon symptomatique", date=d(90), prochaine_date=today + timedelta(days=12))
        Vaccination.objects.create(animal=brebis, produit="Peste des petits ruminants", date=d(200), prochaine_date=today + timedelta(days=160))
        Traitement.objects.create(
            animal=malade, maladie="Parasites internes", produit="Ivermectine", dosage="1 ml / 50 kg",
            date_debut=d(2), date_fin=today + timedelta(days=3), veterinaire="Dr Keïta",
        )

        VenteAnimal.objects.create(animal=chevre, acheteur="Boucherie Centrale", prix=60000, date=d(15))
        PerteAnimal.objects.create(animal=malade.__class__.objects.create(
            sexe="F", espece=ovin, ferme=ferme2, date_naissance=d(500)), type="mortalite", cause="Maladie", date=d(25))
        Depense.objects.create(ferme=ferme, categorie="alimentation", motif="Tourteau de coton", montant=85000, date=d(20))
        Depense.objects.create(ferme=ferme2, categorie="soins", motif="Visite vétérinaire", montant=25000, date=d(8))

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées. Connexion : demo / demo12345"))
