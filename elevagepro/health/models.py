from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Vaccination(models.Model):
    animal = models.ForeignKey(
        "animals.Animal", on_delete=models.CASCADE, related_name="vaccinations", verbose_name="animal"
    )
    produit = models.CharField("vaccin / produit", max_length=120)
    date = models.DateField("date", default=timezone.localdate)
    prochaine_date = models.DateField("prochaine date (rappel)", null=True, blank=True)
    veterinaire = models.CharField("vétérinaire", max_length=120, blank=True)
    observations = models.TextField("observations", blank=True)

    class Meta:
        verbose_name = "vaccination"
        verbose_name_plural = "vaccinations"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.produit} — {self.animal} ({self.date:%d/%m/%Y})"

    def clean(self):
        if self.date and self.prochaine_date and self.prochaine_date <= self.date:
            raise ValidationError({"prochaine_date": "Le rappel doit être postérieur à la date de vaccination."})


class Traitement(models.Model):
    animal = models.ForeignKey(
        "animals.Animal", on_delete=models.CASCADE, related_name="traitements", verbose_name="animal"
    )
    maladie = models.CharField("maladie / motif", max_length=150)
    produit = models.CharField("médicament / produit", max_length=120)
    dosage = models.CharField("dosage", max_length=80, blank=True)
    date_debut = models.DateField("début", default=timezone.localdate)
    date_fin = models.DateField("fin", null=True, blank=True)
    veterinaire = models.CharField("vétérinaire", max_length=120, blank=True)
    observations = models.TextField("observations", blank=True)

    class Meta:
        verbose_name = "traitement vétérinaire"
        verbose_name_plural = "traitements vétérinaires"
        ordering = ["-date_debut", "-id"]

    def __str__(self):
        return f"{self.produit} ({self.maladie}) — {self.animal}"

    def clean(self):
        if self.date_debut and self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError({"date_fin": "La fin ne peut pas précéder le début du traitement."})
