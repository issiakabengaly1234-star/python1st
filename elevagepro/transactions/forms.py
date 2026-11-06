from core.forms import BaseForm, only_present_animals

from .models import Achat, Depense, PerteAnimal, VenteAnimal


class AchatForm(BaseForm):
    class Meta:
        model = Achat
        fields = ["animal", "vendeur", "prix", "date"]


class VenteForm(BaseForm):
    class Meta:
        model = VenteAnimal
        fields = ["animal", "acheteur", "prix", "date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        only_present_animals(self)


class PerteForm(BaseForm):
    class Meta:
        model = PerteAnimal
        fields = ["animal", "type", "cause", "date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        only_present_animals(self)


class DepenseForm(BaseForm):
    class Meta:
        model = Depense
        fields = ["ferme", "categorie", "motif", "montant", "date"]
