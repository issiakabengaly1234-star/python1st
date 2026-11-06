# ÉlevagePro — gestion d'une ferme d'élevage

Application Django de suivi administratif et opérationnel du cheptel :
éleveurs et fermes, espèces et animaux (identifiant unique), naissances,
mouvements, vaccinations, traitements vétérinaires, achats, ventes,
pertes et mortalités, dépenses, effectifs par espèce et historique.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations accounts farms animals health transactions
python manage.py migrate
python manage.py createsuperuser          # ou : python manage.py seed_demo
python manage.py runserver
```

Ouvrez http://127.0.0.1:8000/.
`seed_demo` crée le compte **demo / demo12345** avec deux fermes et des données d'exemple.

## Organisation

| Application    | Contenu                                                                 |
|----------------|-------------------------------------------------------------------------|
| `accounts`     | `Eleveur` (profil lié à l'utilisateur), inscription, connexion, profil  |
| `farms`        | `Ferme`                                                                 |
| `animals`      | `Espece`, `Animal`, `Naissance`, `MouvementAnimal`, fiche animal        |
| `health`       | `Vaccination`, `Traitement`                                             |
| `transactions` | `Achat`, `VenteAnimal`, `PerteAnimal`, `Depense`                        |
| `dashboard`    | Tableau de bord (effectifs, finances, rappels) et historique du cheptel |
| `core`         | Fabrique de vues CRUD, formulaires de base, filtres de templates        |

## Règles métier

- Chaque éleveur ne voit que ses propres fermes et animaux (superutilisateur : tout).
- L'identifiant d'un animal est généré si le champ est laissé vide (ex. `BOV-0001`).
- Enregistrer une **vente** passe l'animal au statut « Vendu » ; une **perte** ou
  **mortalité** le passe à « Mort » ou « Perdu ». Supprimer l'opération rétablit « Présent ».
- Seuls les animaux présents peuvent être vendus ou déclarés perdus.
- La mère d'un animal ou d'une naissance doit être une femelle (même espèce pour la filiation).
- Les rappels de vaccination affichent les échéances à 30 jours ou en retard, sauf si
  le même vaccin a été refait depuis.
- Une ferme ou une espèce qui contient encore des animaux ne peut pas être supprimée.

## Configuration

Variables d'environnement : `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` (`0` en production),
`DJANGO_ALLOWED_HOSTS`, `ELEVAGEPRO_DEVISE` (défaut : `FCFA`).
Fuseau horaire : `Africa/Bamako` (modifiable dans `config/settings.py`).
