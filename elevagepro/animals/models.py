from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Espece(models.Model):
    nom = models.CharField("nom", max_length=80, unique=True)
    description = models.TextField("description", blank=True)

    class Meta:
        verbose_name = "espèce"
        verbose_name_plural = "espèces"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Animal(models.Model):
    PRESENT, VENDU, MORT, PERDU = "present", "vendu", "mort", "perdu"
    STATUTS = [
        (PRESENT, "Présent"),
        (VENDU, "Vendu"),
        (MORT, "Mort"),
        (PERDU, "Perdu"),
    ]
    SEXES = [("M", "Mâle"), ("F", "Femelle")]

    code = models.CharField(
        "identifiant", max_length=30, unique=True, blank=True,
        help_text="Laissez vide pour générer un identifiant automatiquement (ex. BOV-0001).",
    )
    nom = models.CharField("nom ou surnom", max_length=60, blank=True)
    sexe = models.CharField("sexe", max_length=1, choices=SEXES)
    date_naissance = models.DateField("date de naissance", null=True, blank=True)
    espece = models.ForeignKey(Espece, on_delete=models.PROTECT, related_name="animaux", verbose_name="espèce")
    ferme = models.ForeignKey("farms.Ferme", on_delete=models.PROTECT, related_name="animaux", verbose_name="ferme")
    mere = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="descendants", verbose_name="mère",
    )
    statut = models.CharField("statut", max_length=10, choices=STATUTS, default=PRESENT)

    class Meta:
        verbose_name = "animal"
        verbose_name_plural = "animaux"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} · {self.nom}" if self.nom else self.code

    def clean(self):
        if self.mere_id:
            if self.pk and self.mere_id == self.pk:
                raise ValidationError({"mere": "Un animal ne peut pas être sa propre mère."})
            if self.mere.sexe != "F":
                raise ValidationError({"mere": "La mère doit être une femelle."})
            if self.espece_id and self.mere.espece_id != self.espece_id:
                raise ValidationError({"mere": "La mère doit être de la même espèce."})
        if self.date_naissance and self.date_naissance > timezone.localdate():
            raise ValidationError({"date_naissance": "La date de naissance ne peut pas être dans le futur."})

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._generate_code()
        super().save(*args, **kwargs)

    def _generate_code(self):
        prefix = slugify(self.espece.nom)[:3].upper() or "ANI"
        number = Animal.objects.filter(espece=self.espece).count() + 1
        while Animal.objects.filter(code=f"{prefix}-{number:04d}").exists():
            number += 1
        return f"{prefix}-{number:04d}"

    @property
    def age(self):
        if not self.date_naissance:
            return ""
        today = date.today()
        months = (today.year - self.date_naissance.year) * 12 + today.month - self.date_naissance.month
        if today.day < self.date_naissance.day:
            months -= 1
        years, months = divmod(max(months, 0), 12)
        if years:
            return f"{years} an{'s' if years > 1 else ''}" + (f" {months} mois" if months else "")
        return f"{months} mois"


class Naissance(models.Model):
    mere = models.ForeignKey(
        Animal, on_delete=models.CASCADE, related_name="naissances",
        limit_choices_to={"sexe": "F"}, verbose_name="mère",
    )
    date = models.DateField("date", default=timezone.localdate)
    nombre = models.PositiveSmallIntegerField("nombre de petits", default=1, validators=[MinValueValidator(1)])
    observations = models.TextField("observations", blank=True)

    class Meta:
        verbose_name = "naissance"
        verbose_name_plural = "naissances"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.nombre} petit(s) de {self.mere} le {self.date:%d/%m/%Y}"

    def clean(self):
        if self.mere_id and self.mere.sexe != "F":
            raise ValidationError({"mere": "La mère doit être une femelle."})
        if self.date and self.date > timezone.localdate():
            raise ValidationError({"date": "La date ne peut pas être dans le futur."})


class MouvementAnimal(models.Model):
    ENTREE, SORTIE, TRANSFERT = "entree", "sortie", "transfert"
    TYPES = [(ENTREE, "Entrée"), (SORTIE, "Sortie"), (TRANSFERT, "Transfert")]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="mouvements", verbose_name="animal")
    type = models.CharField("type", max_length=10, choices=TYPES)
    date = models.DateField("date", default=timezone.localdate)
    origine = models.CharField("origine", max_length=150, blank=True)
    destination = models.CharField("destination", max_length=150, blank=True)
    observations = models.TextField("observations", blank=True)

    class Meta:
        verbose_name = "mouvement d'animal"
        verbose_name_plural = "mouvements d'animaux"
        ordering = ["-date", "-id"]

    def __str__(self):
        return f"{self.get_type_display()} — {self.animal} ({self.date:%d/%m/%Y})"
