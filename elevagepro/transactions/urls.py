from core.crud import crud

from .forms import AchatForm, DepenseForm, PerteForm, VenteForm
from .models import Achat, Depense, PerteAnimal, VenteAnimal

ANIMAL_OWNER = "animal__ferme__proprietaire__user"

urlpatterns = crud(
    Achat, AchatForm, slug="achat", route="achats",
    title="Achats d'animaux", new_label="Nouvel achat",
    columns=[("Date", "date"), ("Animal", "animal"), ("Vendeur", "vendeur"), ("Prix", "prix", "money")],
    owner=ANIMAL_OWNER, search=("animal__code", "animal__nom", "vendeur"), related=("animal",),
)

urlpatterns += crud(
    VenteAnimal, VenteForm, slug="vente", route="ventes",
    title="Ventes d'animaux", new_label="Nouvelle vente",
    columns=[("Date", "date"), ("Animal", "animal"), ("Acheteur", "acheteur"), ("Prix", "prix", "money")],
    owner=ANIMAL_OWNER, search=("animal__code", "animal__nom", "acheteur"), related=("animal",),
)

urlpatterns += crud(
    PerteAnimal, PerteForm, slug="perte", route="pertes",
    title="Pertes et mortalités", new_label="Nouvelle perte",
    columns=[("Date", "date"), ("Animal", "animal"), ("Type", "get_type_display"), ("Cause", "cause")],
    owner=ANIMAL_OWNER, search=("animal__code", "animal__nom", "cause"), related=("animal",),
    chips=("type", PerteAnimal.TYPES),
)

urlpatterns += crud(
    Depense, DepenseForm, slug="depense", route="depenses",
    title="Dépenses", new_label="Nouvelle dépense",
    columns=[
        ("Date", "date"),
        ("Ferme", "ferme"),
        ("Catégorie", "get_categorie_display"),
        ("Motif", "motif"),
        ("Montant", "montant", "money"),
    ],
    owner="ferme__proprietaire__user", search=("motif", "ferme__nom"), related=("ferme",),
    chips=("categorie", Depense.CATEGORIES),
)
