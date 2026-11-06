from .models import Eleveur


def get_eleveur(user):
    eleveur, _ = Eleveur.objects.get_or_create(
        user=user, defaults={"nom": user.get_full_name() or user.get_username()}
    )
    return eleveur
