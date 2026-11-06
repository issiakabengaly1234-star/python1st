from django.urls import path

from core.crud import crud

from . import views
from .forms import AnimalForm, EspeceForm, MouvementForm, NaissanceForm
from .models import Animal, Espece, MouvementAnimal, Naissance

urlpatterns = [
    path("animaux/<int:pk>/", views.AnimalDetailView.as_view(), name="animal_detail"),
]

urlpatterns += crud(
    Espece, EspeceForm, slug="espece", route="especes",
    title="Espèces", new_label="Nouvelle espèce",
    columns=[("Nom", "nom"), ("Description", "description"), ("Animaux", "animaux.count")],
    search=("nom", "description"),
)

urlpatterns += crud(
    Animal, AnimalForm, slug="animal", route="animaux",
    title="Animaux", new_label="Nouvel animal",
    columns=[
        ("Identifiant", "code"),
        ("Nom", "nom"),
        ("Espèce", "espece"),
        ("Sexe", "get_sexe_display"),
        ("Ferme", "ferme"),
        ("Naissance", "date_naissance"),
        ("Statut", "get_statut_display", "badge"),
    ],
    owner="ferme__proprietaire__user", search=("code", "nom", "espece__nom"),
    related=("espece", "ferme"), chips=("statut", Animal.STATUTS), detail="animal_detail",
)

urlpatterns += crud(
    Naissance, NaissanceForm, slug="naissance", route="naissances",
    title="Naissances", new_label="Nouvelle naissance",
    columns=[("Date", "date"), ("Mère", "mere"), ("Petits", "nombre"), ("Observations", "observations")],
    owner="mere__ferme__proprietaire__user", search=("mere__code", "mere__nom", "observations"),
    related=("mere",),
)

urlpatterns += crud(
    MouvementAnimal, MouvementForm, slug="mouvement", route="mouvements",
    title="Mouvements d'animaux", new_label="Nouveau mouvement",
    columns=[
        ("Date", "date"),
        ("Animal", "animal"),
        ("Type", "get_type_display"),
        ("Origine", "origine"),
        ("Destination", "destination"),
    ],
    owner="animal__ferme__proprietaire__user",
    search=("animal__code", "animal__nom", "origine", "destination"), related=("animal",),
    chips=("type", MouvementAnimal.TYPES),
)
