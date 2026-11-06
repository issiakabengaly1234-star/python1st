from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Exists, OuterRef, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from animals.models import Animal, Naissance
from farms.models import Ferme
from health.models import Traitement, Vaccination
from transactions.models import Achat, Depense, PerteAnimal, VenteAnimal

from .services import KINDS, build_timeline


def user_fermes(user):
    qs = Ferme.objects.all()
    return qs if user.is_superuser else qs.filter(proprietaire__user=user)


def selected_scope(request):
    """Retourne (toutes les fermes de l'utilisateur, ferme choisie ou None, fermes concernées)."""
    fermes = user_fermes(request.user)
    raw = request.GET.get("ferme", "")
    selected = fermes.filter(pk=raw).first() if raw.isdigit() else None
    scope = fermes.filter(pk=selected.pk) if selected else fermes
    return fermes, selected, scope


def total(qs, field):
    return qs.aggregate(t=Sum(field))["t"] or Decimal("0")


@login_required
def index(request):
    fermes, selected, scope = selected_scope(request)
    today = timezone.localdate()
    year = today.year
    animaux = Animal.objects.filter(ferme__in=scope)
    presents = animaux.filter(statut=Animal.PRESENT)

    effectifs = list(
        presents.values("espece__nom")
        .annotate(
            total=Count("id"),
            males=Count("id", filter=Q(sexe="M")),
            femelles=Count("id", filter=Q(sexe="F")),
        )
        .order_by("-total", "espece__nom")
    )
    biggest = max((e["total"] for e in effectifs), default=1)
    for e in effectifs:
        e["pct"] = round(100 * e["total"] / biggest)

    ventes = VenteAnimal.objects.filter(animal__ferme__in=scope, date__year=year)
    achats = Achat.objects.filter(animal__ferme__in=scope, date__year=year)
    depenses = Depense.objects.filter(ferme__in=scope, date__year=year)
    total_ventes, total_achats, total_depenses = total(ventes, "prix"), total(achats, "prix"), total(depenses, "montant")

    plus_tard = Vaccination.objects.filter(
        animal=OuterRef("animal"), produit=OuterRef("produit"), date__gt=OuterRef("date")
    )
    rappels = list(
        Vaccination.objects.filter(
            animal__ferme__in=scope,
            animal__statut=Animal.PRESENT,
            prochaine_date__isnull=False,
            prochaine_date__lte=today + timedelta(days=30),
        )
        .filter(~Exists(plus_tard))
        .select_related("animal")
        .order_by("prochaine_date")[:10]
    )
    for r in rappels:
        r.en_retard = r.prochaine_date < today

    traitements = (
        Traitement.objects.filter(
            animal__ferme__in=scope, animal__statut=Animal.PRESENT,
            date_debut__lte=today, date_fin__gte=today,
        )
        .select_related("animal")
        .order_by("date_fin")[:8]
    )

    context = {
        "fermes": fermes,
        "selected": selected,
        "year": year,
        "effectif_total": presents.count(),
        "effectifs": effectifs,
        "naissances": Naissance.objects.filter(mere__ferme__in=scope, date__year=year).aggregate(n=Sum("nombre"))["n"] or 0,
        "pertes": PerteAnimal.objects.filter(animal__ferme__in=scope, date__year=year).count(),
        "nb_ventes": ventes.count(),
        "total_ventes": total_ventes,
        "total_sorties": total_achats + total_depenses,
        "solde": total_ventes - total_achats - total_depenses,
        "rappels": rappels,
        "traitements": traitements,
        "recents": build_timeline(scope, limit=8),
    }
    return render(request, "dashboard/index.html", context)


@login_required
def historique(request):
    fermes, selected, scope = selected_scope(request)
    valid = {k for k, _ in KINDS}
    kind = request.GET.get("type", "")
    events = build_timeline(scope, kinds=[kind] if kind in valid else None, limit=300)
    return render(request, "dashboard/historique.html", {
        "fermes": fermes, "selected": selected, "kinds": KINDS, "kind": kind, "events": events,
    })
