from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils import timezone


def prix_field(label):
    return models.DecimalField(label, max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])


class Achat(models.Model):
    animal = models.ForeignKey("animals.Animal", on_delete=models.CASCADE, related_name="achats", verbose_name="animal")
    vendeur = models.CharField("vendeur", max_length=150)
    prix = prix_field("prix")
    date = models.DateField("date", default=timezone.localdate)

    class Meta:
        verbose_name = "achat d'animal"
        verbose_name_plural = "achats d'animaux"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"Achat {self.animal} ({self.date:%d/%m/%Y})"


class VenteAnimal(models.Model):
    animal = models.ForeignKey("animals.Animal", on_delete=models.CASCADE, related_name="ventes", verbose_name="animal")
    acheteur = models.CharField("acheteur", max_length=150)
    prix = prix_field("prix")
    date = models.DateField("date", default=timezone.localdate)

    class Meta:
        verbose_name = "vente d'animal"
        verbose_name_plural = "ventes d'animaux"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"Vente {self.animal} ({self.date:%d/%m/%Y})"

    def clean(self):
        if self.animal_id and not self.pk and self.animal.statut != "present":
            raise ValidationError({"animal": "Cet animal n'est plus présent dans le cheptel."})

    def save(self, *args, **kwargs):
        creating = self._state.adding
        with transaction.atomic():
            super().save(*args, **kwargs)
            if creating:
                self.animal.__class__.objects.filter(pk=self.animal_id).update(statut="vendu")

    def delete(self, *args, **kwargs):
        animal_model, animal_id = self.animal.__class__, self.animal_id
        with transaction.atomic():
            result = super().delete(*args, **kwargs)
            if not VenteAnimal.objects.filter(animal_id=animal_id).exists():
                animal_model.objects.filter(pk=animal_id, statut="vendu").update(statut="present")
        return result


class PerteAnimal(models.Model):
    MORTALITE, PERTE = "mortalite", "perte"
    TYPES = [(MORTALITE, "Mortalité"), (PERTE, "Perte (vol, disparition…)")]

    animal = models.ForeignKey("animals.Animal", on_delete=models.CASCADE, related_name="pertes", verbose_name="animal")
    type = models.CharField("type", max_length=10, choices=TYPES, default=MORTALITE)
    cause = models.CharField("cause", max_length=200, blank=True)
    date = models.DateField("date", default=timezone.localdate)

    class Meta:
        verbose_name = "perte ou mortalité"
        verbose_name_plural = "pertes et mortalités"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.get_type_display()} — {self.animal} ({self.date:%d/%m/%Y})"

    def clean(self):
        if self.animal_id and not self.pk and self.animal.statut != "present":
            raise ValidationError({"animal": "Cet animal n'est plus présent dans le cheptel."})

    def _statut(self):
        return "mort" if self.type == self.MORTALITE else "perdu"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.animal.__class__.objects.filter(pk=self.animal_id).update(statut=self._statut())

    def delete(self, *args, **kwargs):
        animal_model, animal_id = self.animal.__class__, self.animal_id
        with transaction.atomic():
            result = super().delete(*args, **kwargs)
            if not PerteAnimal.objects.filter(animal_id=animal_id).exists():
                animal_model.objects.filter(pk=animal_id, statut__in=["mort", "perdu"]).update(statut="present")
        return result


class Depense(models.Model):
    CATEGORIES = [
        ("alimentation", "Alimentation"),
        ("soins", "Soins vétérinaires"),
        ("main_oeuvre", "Main-d'œuvre"),
        ("equipement", "Équipement et bâtiments"),
        ("autre", "Autre"),
    ]

    ferme = models.ForeignKey("farms.Ferme", on_delete=models.CASCADE, related_name="depenses", verbose_name="ferme")
    categorie = models.CharField("catégorie", max_length=20, choices=CATEGORIES, default="autre")
    motif = models.CharField("motif", max_length=200)
    montant = prix_field("montant")
    date = models.DateField("date", default=timezone.localdate)

    class Meta:
        verbose_name = "dépense"
        verbose_name_plural = "dépenses"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.motif} ({self.date:%d/%m/%Y})"
