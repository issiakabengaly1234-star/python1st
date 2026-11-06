from django.contrib import admin

from .models import Eleveur


@admin.register(Eleveur)
class EleveurAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "localisation", "user")
    search_fields = ("nom", "telephone", "localisation")
