from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import EleveurForm, RegisterForm
from .helpers import get_eleveur


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Compte créé. Commencez par ajouter votre première ferme.")
        return redirect("ferme_create")
    return render(request, "accounts/register.html", {"form": form})


class ProfilView(LoginRequiredMixin, UpdateView):
    form_class = EleveurForm
    template_name = "accounts/profil.html"
    success_url = reverse_lazy("profil")

    def get_object(self, queryset=None):
        return get_eleveur(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Profil mis à jour.")
        return super().form_valid(form)
