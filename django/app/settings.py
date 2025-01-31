"""
Django settings for app project.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = os.environ.get("SECRET_KEY")

VENDOR_API_KEY = os.environ.get("VENDOR_API_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(" ")


# Application definition

INSTALLED_APPS = [
    "rest_framework",
    "knox",
    "corsheaders",
    "django_celery_beat",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get(
            "SQL_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "NAME": os.environ.get("SQL_NAME", "postgres"),
        "USER": os.environ.get("SQL_USER", "postgres"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "postgres"),
        "HOST": os.environ.get("SQL_HOST", "db-primary"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    },
    "celerybeat": {
        "ENGINE": os.environ.get(
            "DJANGO_SQL_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "NAME": os.environ.get("DJANGO_SQL_NAME", "postgres"),
        "USER": os.environ.get("DJANGO_SQL_USER", "postgres"),
        "PASSWORD": os.environ.get("DJANGO_SQL_PASSWORD", "postgres"),
        "HOST": os.environ.get("DJANGO_SQL_HOST", "db-celerybeat"),
        "PORT": os.environ.get("DJANGO_SQL_PORT", "5432"),
    },
}

DATABASE_ROUTERS = [
    "app.db.routers.CeleryBeatRouter",
]

# Add support for database replica in production environments.
if not DEBUG:
    DATABASES["replica"] = {
        "ENGINE": os.environ.get(
            "SQL_ENGINE", "django.db.backends.postgresql_psycopg2"
        ),
        "NAME": os.environ.get("SQL_NAME", "postgres"),
        "USER": os.environ.get("SQL_USER", "postgres"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "postgres"),
        "HOST": os.environ.get("SQL_HOST", "db-replica"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }

    DATABASE_ROUTERS += [
        "app.db.routers.ReplicationRouter",
    ]


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CACHES = {
    "default": {
        "BACKEND": os.environ.get(
            "CACHE_BACKEND", "django.core.cache.backends.redis.RedisCache"
        ),
        "LOCATION": os.environ.get("CACHE_BACKEND", "redis://redis:6379"),
    }
}

PRICE_CACHE_TTL = 5
SEARCH_CACHE_TTL = 60 * 5
WATCHLIST_CACHE_TTL = 60 * 60

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
}

REST_KNOX = {
    "USER_SERIALIZER": "knox.serializers.UserSerializer",
    "TOKEN_LIMIT_PER_USER": int(os.environ.get("KNOX_TOKEN_LIMIT", 1)),
    "TOKEN_TTL": timedelta(
        days=int(os.environ.get("KNOX_TOKEN_TTL_DAYS", 0)),
        hours=int(os.environ.get("KNOX_TOKEN_TTL_HOURS", 10)),
    ),
}

# https://docs.celeryq.dev/en/latest/userguide/configuration.html
CELERY_RESULT_PERSISTENT = bool(os.environ.get("CELERY_RESULT_PERSISTENT", default=1))
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "amqp://rabbitmq:5672")

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"