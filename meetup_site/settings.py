from pathlib import Path
import os

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings for development
SECRET_KEY = "django-insecure-meetup-secret-key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Installed apps: Django built-ins + our custom events app
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "events",
]

# Middleware used to process requests and responses
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Tell Django where the main URL routes are defined
ROOT_URLCONF = "meetup_site.urls"

# Template settings so HTML pages can be rendered
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "meetup_site.wsgi.application"

# MySQL database configuration for the meetup app
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "meetup_db",
        "USER": "django_user",
        "PASSWORD": "StrongPassword123!",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

# Password rules for user accounts
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# General site settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Redirect users after login/logout
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "event_list"
LOGOUT_REDIRECT_URL = "login"
