from django.contrib import admin

from .models import Animal, Espece, MouvementAnimal, Naissance


@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = ("nom", "description")
    search_fields = ("nom",)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ("code", "nom", "espece", "sexe", "ferme", "date_naissance", "statut")
    list_filter = ("espece", "sexe", "statut", "ferme")
    search_fields = ("code", "nom")


@admin.register(Naissance)
class NaissanceAdmin(admin.ModelAdmin):
    list_display = ("date", "mere", "nombre")
    list_filter = ("date",)


@admin.register(MouvementAnimal)
class MouvementAdmin(admin.ModelAdmin):
    list_display = ("date", "animal", "type", "origine", "destination")
    list_filter = ("type", "date")
