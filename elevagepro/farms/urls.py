from accounts.helpers import get_eleveur
from core.crud import crud

from .forms import FermeForm
from .models import Ferme


def set_owner(request, ferme):
    ferme.proprietaire = get_eleveur(request.user)


urlpatterns = crud(
    Ferme, FermeForm, slug="ferme", route="fermes",
    title="Fermes", new_label="Nouvelle ferme",
    columns=[
        ("Nom", "nom"),
        ("Propriétaire", "proprietaire"),
        ("Localisation", "localisation"),
        ("Effectif actuel", "effectif"),
    ],
    owner="proprietaire__user", search=("nom", "localisation"),
    related=("proprietaire",), on_create=set_owner,
)
