from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from core.crud import owned

from .models import Animal


class AnimalDetailView(LoginRequiredMixin, DetailView):
    template_name = "animals/animal_detail.html"

    def get_queryset(self):
        qs = Animal.objects.select_related("espece", "ferme", "mere")
        return owned(qs, self.request.user, "ferme__proprietaire__user")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        a = self.object
        ctx.update(
            naissances=a.naissances.all(),
            descendants=a.descendants.select_related("espece"),
            mouvements=a.mouvements.all(),
            vaccinations=a.vaccinations.all(),
            traitements=a.traitements.all(),
            achats=a.achats.all(),
            ventes=a.ventes.all(),
            pertes=a.pertes.all(),
        )
        return ctx
