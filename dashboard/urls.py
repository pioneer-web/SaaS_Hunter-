from django.urls import path

from .views import (
    home,
    opportunities_page,
    repositories_page,
    run_scan,
)

app_name = "dashboard"

urlpatterns = [
    path("", home, name="home"),
    path("repositorios/", repositories_page, name="repositories"),
    path("oportunidades/", opportunities_page, name="opportunities"),
    path("executar-caca/", run_scan, name="run_scan"),
]
