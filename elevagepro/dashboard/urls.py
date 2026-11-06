from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dashboard"),
    path("historique/", views.historique, name="historique"),
]
