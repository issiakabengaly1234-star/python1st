from core.forms import BaseForm

from .models import Ferme


class FermeForm(BaseForm):
    class Meta:
        model = Ferme
        fields = ["nom", "localisation"]
