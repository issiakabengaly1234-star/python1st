from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.forms import BaseForm

from .models import Eleveur, phone_validator

User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Prénom", max_length=60)
    last_name = forms.CharField(label="Nom", max_length=60)
    telephone = forms.CharField(
        label="Téléphone", max_length=20, required=False, validators=[phone_validator]
    )
    localisation = forms.CharField(label="Localisation", max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            eleveur = user.eleveur  # créé par le signal post_save
            eleveur.nom = f"{user.first_name} {user.last_name}".strip()
            eleveur.telephone = self.cleaned_data["telephone"]
            eleveur.localisation = self.cleaned_data["localisation"]
            eleveur.save()
        return user


class EleveurForm(BaseForm):
    class Meta:
        model = Eleveur
        fields = ["nom", "telephone", "localisation"]
