from django import forms
from django.db.models import Q


class BaseForm(forms.ModelForm):
    """ModelForm commun : champs date HTML5 et zones de texte compactes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.DateField):
                field.widget = forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs["rows"] = 3


def only_present_animals(form):
    """Limite le champ « animal » aux animaux présents (ou à celui déjà enregistré)."""
    from animals.models import Animal

    condition = Q(statut=Animal.PRESENT)
    if form.instance.pk and form.instance.animal_id:
        condition |= Q(pk=form.instance.animal_id)
    form.fields["animal"].queryset = Animal.objects.filter(condition)
