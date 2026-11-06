from django.contrib import admin

from .models import Achat, Depense, PerteAnimal, VenteAnimal


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ("date", "animal", "vendeur", "prix")
    search_fields = ("animal__code", "vendeur")


@admin.register(VenteAnimal)
class VenteAdmin(admin.ModelAdmin):
    list_display = ("date", "animal", "acheteur", "prix")
    search_fields = ("animal__code", "acheteur")


@admin.register(PerteAnimal)
class PerteAdmin(admin.ModelAdmin):
    list_display = ("date", "animal", "type", "cause")
    list_filter = ("type",)


@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ("date", "ferme", "categorie", "motif", "montant")
    list_filter = ("categorie", "ferme")
