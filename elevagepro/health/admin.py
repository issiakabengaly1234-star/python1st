from django.contrib import admin

from .models import Traitement, Vaccination


@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ("date", "animal", "produit", "prochaine_date", "veterinaire")
    list_filter = ("produit", "date")
    search_fields = ("animal__code", "produit")


@admin.register(Traitement)
class TraitementAdmin(admin.ModelAdmin):
    list_display = ("date_debut", "date_fin", "animal", "maladie", "produit")
    list_filter = ("date_debut",)
    search_fields = ("animal__code", "maladie", "produit")
