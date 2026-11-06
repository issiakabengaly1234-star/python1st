from django import template

from core.utils import format_money

register = template.Library()


@register.filter
def attr(obj, path):
    """Résout un chemin pointé (« espece.nom », « get_sexe_display ») sur un objet."""
    for part in str(path).split("."):
        if obj is None:
            return None
        obj = getattr(obj, part, None)
        # Les gestionnaires de relations (ex. espece.animaux) sont « callable » : on ne les appelle pas.
        if callable(obj) and not hasattr(obj, "model"):
            obj = obj()
    return None if obj == "" else obj


@register.filter
def money(value):
    return format_money(value)
