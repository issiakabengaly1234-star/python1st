from core.forms import BaseForm

from .models import Traitement, Vaccination


class VaccinationForm(BaseForm):
    class Meta:
        model = Vaccination
        fields = ["animal", "produit", "date", "prochaine_date", "veterinaire", "observations"]


class TraitementForm(BaseForm):
    class Meta:
        model = Traitement
        fields = ["animal", "maladie", "produit", "dosage", "date_debut", "date_fin", "veterinaire", "observations"]
