from django.urls import reverse

GROUPS = [
    ("Exploitation", [
        ("Tableau de bord", "dashboard"),
        ("Historique du cheptel", "historique"),
        ("Fermes", "ferme_list"),
    ]),
    ("Cheptel", [
        ("Animaux", "animal_list"),
        ("Espèces", "espece_list"),
        ("Naissances", "naissance_list"),
        ("Mouvements", "mouvement_list"),
    ]),
    ("Santé", [
        ("Vaccinations", "vaccination_list"),
        ("Traitements", "traitement_list"),
    ]),
    ("Finances", [
        ("Achats", "achat_list"),
        ("Ventes", "vente_list"),
        ("Pertes et mortalités", "perte_list"),
        ("Dépenses", "depense_list"),
    ]),
]


def navigation(request):
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        return {}
    groups = []
    for label, items in GROUPS:
        rows = []
        for text, name in items:
            url = reverse(name)
            active = request.path == url if name == "dashboard" else request.path.startswith(url)
            rows.append({"text": text, "url": url, "active": active})
        groups.append({"label": label, "items": rows})
    return {"nav_groups": groups}
