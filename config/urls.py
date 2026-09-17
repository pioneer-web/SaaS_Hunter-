from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from core.views import health

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="/login/"),
        name="logout",
    ),

    path("admin/", admin.site.urls),
    path("health/", health, name="health"),

    path("", include("dashboard.urls")),
]
