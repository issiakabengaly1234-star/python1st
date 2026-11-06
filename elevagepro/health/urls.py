from core.crud import crud

from .forms import TraitementForm, VaccinationForm
from .models import Traitement, Vaccination

OWNER = "animal__ferme__proprietaire__user"

urlpatterns = crud(
    Vaccination, VaccinationForm, slug="vaccination", route="vaccinations",
    title="Vaccinations", new_label="Nouvelle vaccination",
    columns=[
        ("Date", "date"),
        ("Animal", "animal"),
        ("Produit", "produit"),
        ("Rappel prévu", "prochaine_date"),
        ("Vétérinaire", "veterinaire"),
    ],
    owner=OWNER, search=("animal__code", "animal__nom", "produit", "veterinaire"), related=("animal",),
)

urlpatterns += crud(
    Traitement, TraitementForm, slug="traitement", route="traitements",
    title="Traitements vétérinaires", new_label="Nouveau traitement",
    columns=[
        ("Début", "date_debut"),
        ("Fin", "date_fin"),
        ("Animal", "animal"),
        ("Maladie", "maladie"),
        ("Produit", "produit"),
        ("Dosage", "dosage"),
    ],
    owner=OWNER, search=("animal__code", "animal__nom", "maladie", "produit"), related=("animal",),
)
