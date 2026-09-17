import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def env(name, default=None):
    return os.getenv(name, default)

SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = env("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    x.strip() for x in env(
        "DJANGO_ALLOWED_HOSTS",
        "hunter.confronta.com.br,localhost,127.0.0.1"
    ).split(",") if x.strip()
]

CSRF_TRUSTED_ORIGINS = [
    x.strip() for x in env(
        "CSRF_TRUSTED_ORIGINS",
        "https://hunter.confronta.com.br"
    ).split(",") if x.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "dashboard",
    "repositories",
    "opportunities",
    "scanner",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", "saas_hunter"),
        "USER": env("POSTGRES_USER", "saas_hunter"),
        "PASSWORD": env("POSTGRES_PASSWORD", ""),
        "HOST": env("POSTGRES_HOST", "db"),
        "PORT": env("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Recife"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

CELERY_BROKER_URL = env("REDIS_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = env("REDIS_URL", "redis://redis:6379/0")
CELERY_TIMEZONE = env("CELERY_TIMEZONE", "America/Recife")
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_BEAT_SCHEDULE = {
    "github-discovery-every-6-hours": {
        "task": "scanner.tasks.discover_repositories",
        "schedule": 60 * 60 * 6,
    },
    "refresh-snapshots-daily": {
        "task": "scanner.tasks.refresh_repository_snapshots",
        "schedule": 60 * 60 * 24,
    },
    "market-research-daily": {
        "task": "opportunities.tasks.research_top_opportunities",
        "schedule": 60 * 60 * 24,
        "kwargs": {
            "limit": 8,
        },
    },
}


# Arquivos estáticos em produção
WHITENOISE_MAX_AGE = 31536000
WHITENOISE_AUTOREFRESH = False
