from django.contrib import admin

from .models import Ferme


@admin.register(Ferme)
class FermeAdmin(admin.ModelAdmin):
    list_display = ("nom", "proprietaire", "localisation")
    search_fields = ("nom", "localisation", "proprietaire__nom")
    list_filter = ("proprietaire",)
