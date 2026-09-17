from django.urls import path

from .views import (
    home,
    opportunities_page,
    opportunity_detail,
    repositories_page,
    run_market_research,
    run_scan,
)


app_name = "dashboard"


urlpatterns = [

    path(
        "",
        home,
        name="home",
    ),

    path(
        "repositorios/",
        repositories_page,
        name="repositories",
    ),

    path(
        "oportunidades/",
        opportunities_page,
        name="opportunities",
    ),

    path(
        "oportunidades/<int:pk>/",
        opportunity_detail,
        name="opportunity_detail",
    ),

    path(
        "oportunidades/<int:pk>/pesquisar-mercado/",
        run_market_research,
        name="run_market_research",
    ),

    path(
        "executar-caca/",
        run_scan,
        name="run_scan",
    ),
]
