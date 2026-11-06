from django.db import models


class Ferme(models.Model):
    nom = models.CharField("nom", max_length=120)
    proprietaire = models.ForeignKey(
        "accounts.Eleveur", on_delete=models.CASCADE, related_name="fermes", verbose_name="propriétaire"
    )
    localisation = models.CharField("localisation", max_length=150, blank=True)

    class Meta:
        verbose_name = "ferme"
        verbose_name_plural = "fermes"
        ordering = ["nom"]

    def __str__(self):
        return self.nom

    @property
    def effectif(self):
        return self.animaux.filter(statut="present").count()
