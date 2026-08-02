"""WSGI configuration for the Django project.

This module exposes the WSGI application callable used by servers to run the
project in production or development WSGI deployments.
"""

import os
from django.core.wsgi import get_wsgi_application


# Ensure the settings module is set before creating the WSGI application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meetup_site.settings")
application = get_wsgi_application()
