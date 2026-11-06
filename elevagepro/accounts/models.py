from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(r"^\+?[0-9 .\-]{8,20}$", "Numéro de téléphone invalide.")


class Eleveur(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="eleveur"
    )
    nom = models.CharField("nom", max_length=120)
    telephone = models.CharField("téléphone", max_length=20, blank=True, validators=[phone_validator])
    localisation = models.CharField("localisation", max_length=150, blank=True)

    class Meta:
        verbose_name = "éleveur"
        verbose_name_plural = "éleveurs"
        ordering = ["nom"]

    def __str__(self):
        return self.nom
