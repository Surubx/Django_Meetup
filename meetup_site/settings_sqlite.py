"""Local development settings that run the project on SQLite.

This keeps the normal MySQL configuration intact while providing a
friction-free local launcher for Windows development.
"""

from .settings import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "dev_db.sqlite3",
    }
}