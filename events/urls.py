from django.urls import path
from . import views

# URL patterns for the meetup app
urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="account_login"),
    path("logout/", views.logout_view, name="logout"),
    path("accounts/logout/", views.logout_view, name="account_logout"),
    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),
    path("events/<int:pk>/join/", views.join_event, name="join_event"),
    path("events/<int:pk>/leave/", views.leave_event, name="leave_event"),
    path("my-events/", views.my_events, name="my_events"),
    path("reminders/", views.reminder_view, name="reminders"),
]
