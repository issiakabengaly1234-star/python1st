from core.forms import BaseForm

from .models import Animal, Espece, MouvementAnimal, Naissance


class EspeceForm(BaseForm):
    class Meta:
        model = Espece
        fields = ["nom", "description"]


class AnimalForm(BaseForm):
    class Meta:
        model = Animal
        fields = ["code", "nom", "sexe", "date_naissance", "espece", "ferme", "mere"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mere"].queryset = Animal.objects.filter(sexe="F")


class NaissanceForm(BaseForm):
    class Meta:
        model = Naissance
        fields = ["mere", "date", "nombre", "observations"]


class MouvementForm(BaseForm):
    class Meta:
        model = MouvementAnimal
        fields = ["animal", "type", "date", "origine", "destination", "observations"]
