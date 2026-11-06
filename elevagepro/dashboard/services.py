from animals.models import MouvementAnimal, Naissance
from core.utils import format_money
from health.models import Traitement, Vaccination
from transactions.models import Achat, PerteAnimal, VenteAnimal

KINDS = [
    ("naissance", "Naissances"),
    ("mouvement", "Mouvements"),
    ("vaccination", "Vaccinations"),
    ("traitement", "Traitements"),
    ("achat", "Achats"),
    ("vente", "Ventes"),
    ("perte", "Pertes et mortalités"),
]
KIND_LABELS = dict(KINDS)


def build_timeline(fermes, kinds=None, limit=200):
    """Fusionne tous les événements du cheptel en une liste triée du plus récent au plus ancien."""
    kinds = set(kinds) if kinds else set(KIND_LABELS)
    events = []

    def add(date, kind, title, detail="", animal=None):
        events.append({
            "date": date, "kind": kind, "kind_label": KIND_LABELS[kind],
            "title": title, "detail": detail, "animal": animal,
        })

    if "naissance" in kinds:
        for n in Naissance.objects.filter(mere__ferme__in=fermes).select_related("mere"):
            detail = f"Mère : {n.mere}" + (f" — {n.observations}" if n.observations else "")
            add(n.date, "naissance", f"{n.nombre} naissance{'s' if n.nombre > 1 else ''}", detail, n.mere)
    if "mouvement" in kinds:
        for m in MouvementAnimal.objects.filter(animal__ferme__in=fermes).select_related("animal"):
            route = " → ".join(x for x in (m.origine, m.destination) if x)
            add(m.date, "mouvement", f"{m.get_type_display()} : {m.animal}", route, m.animal)
    if "vaccination" in kinds:
        for v in Vaccination.objects.filter(animal__ferme__in=fermes).select_related("animal"):
            detail = f"Rappel prévu le {v.prochaine_date:%d/%m/%Y}" if v.prochaine_date else ""
            add(v.date, "vaccination", f"{v.produit} : {v.animal}", detail, v.animal)
    if "traitement" in kinds:
        for t in Traitement.objects.filter(animal__ferme__in=fermes).select_related("animal"):
            add(t.date_debut, "traitement", f"{t.produit} ({t.maladie}) : {t.animal}", t.dosage, t.animal)
    if "achat" in kinds:
        for a in Achat.objects.filter(animal__ferme__in=fermes).select_related("animal"):
            add(a.date, "achat", f"Achat : {a.animal}", f"{a.vendeur} · {format_money(a.prix)}", a.animal)
    if "vente" in kinds:
        for v in VenteAnimal.objects.filter(animal__ferme__in=fermes).select_related("animal"):
            add(v.date, "vente", f"Vente : {v.animal}", f"{v.acheteur} · {format_money(v.prix)}", v.animal)
    if "perte" in kinds:
        for p in PerteAnimal.objects.filter(animal__ferme__in=fermes).select_related("animal"):
            add(p.date, "perte", f"{p.get_type_display()} : {p.animal}", p.cause, p.animal)

    events.sort(key=lambda e: e["date"], reverse=True)
    return events[:limit]
