"""URL configuration for the Django project.

Routes defined here delegate to the `events` app and the Django admin.
"""

from django.contrib import admin
from django.urls import path, include


# Top-level URL routes for the project. The `events` app handles the main
# application pages while the admin is exposed at /admin/.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("events.urls")),
]
