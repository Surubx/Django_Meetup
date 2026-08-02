"""Test settings used when running the Django test suite locally.

This file imports the main settings and overrides the `DATABASES` setting so
tests run against a temporary SQLite database. This avoids the need for
additional permissions to create MySQL test databases when running CI or
local tests.
"""

from .settings import *

# Use SQLite for running tests so Django can create a temporary test database
# without requiring extra MySQL permissions.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}
