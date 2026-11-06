from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "ÉlevagePro — administration"
admin.site.site_title = "ÉlevagePro"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("", include("accounts.urls")),
    path("", include("farms.urls")),
    path("", include("animals.urls")),
    path("", include("health.urls")),
    path("", include("transactions.urls")),
]
