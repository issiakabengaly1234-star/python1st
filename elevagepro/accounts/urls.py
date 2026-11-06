from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("connexion/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("inscription/", views.register, name="register"),
    path("profil/", views.ProfilView.as_view(), name="profil"),
]
