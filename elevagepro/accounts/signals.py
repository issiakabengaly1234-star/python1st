from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Eleveur


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_eleveur(sender, instance, created, raw=False, **kwargs):
    """Chaque compte utilisateur dispose automatiquement d'un profil d'éleveur."""
    if created and not raw:
        Eleveur.objects.get_or_create(
            user=instance,
            defaults={"nom": instance.get_full_name() or instance.get_username()},
        )
