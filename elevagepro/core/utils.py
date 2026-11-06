from decimal import Decimal

from django.conf import settings


def format_money(value):
    """Formate un montant : 1 250 000 FCFA (sans décimales si entier)."""
    if value in (None, ""):
        return "—"
    value = Decimal(value)
    if value == value.to_integral_value():
        text = f"{value:,.0f}"
    else:
        text = f"{value:,.2f}"
    text = text.replace(",", "\u202f").replace(".", ",")
    return f"{text}\u00a0{settings.DEVISE}"
