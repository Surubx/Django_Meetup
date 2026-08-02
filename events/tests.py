from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event

#To run the tests, use the command:
# .\.venv\Scripts\python.exe manage.py test events --settings=meetup_site.settings_test
"""Test suite for the events app.

These tests include simple unit checks for the Event model and higher-level
workflow tests that exercise the request/response paths (create, join, leave).
The workflow tests run against a temporary test database (configured via
`meetup_site.settings_test` in CI or local test runs).
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event


class EventModelTests(TestCase):
    """Unit tests for `Event` model behavior."""

    def test_event_string_representation(self):
        """The model's __str__ should return the event title."""
        user = get_user_model().objects.create_user(username="organizer", password="secret123")
        event = Event.objects.create(
            title="Tech Meetup",
            description="A friendly meetup for developers.",
            date=timezone.now() + timedelta(days=1),
            location="Nairobi",
            organizer=user,
        )

        self.assertEqual(str(event), "Tech Meetup")


class EventWorkflowTests(TestCase):
    """Higher-level tests that simulate user actions via the test client."""

    def setUp(self):
        # Create two users and one sample event organized by `self.user`.
        self.user = get_user_model().objects.create_user(username="alice", password="secret123")
        self.other_user = get_user_model().objects.create_user(username="bob", password="secret123")
        self.event = Event.objects.create(
            title="Community Meetup",
            description="Discussing local community events.",
            date=timezone.now() + timedelta(days=2),
            location="Kampala",
            organizer=self.user,
        )

    def test_login_required_for_event_listing(self):
        """Unauthenticated users should be redirected to the login page."""
        response = self.client.get(reverse("event_list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_user_can_create_event(self):
        """Logged-in users can create events using the event create view."""
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("event_create"),
            {
                "title": "New Workshop",
                "description": "Hands-on Django workshop",
                "date": (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
                "location": "Lagos",
            },
            follow=True,
        )

        self.assertContains(response, "Event created successfully!")
        self.assertTrue(Event.objects.filter(title="New Workshop", organizer=self.user).exists())

    def test_user_can_join_and_leave_event(self):
        """A user should be able to join and later leave an event."""
        self.client.force_login(self.other_user)

        join_response = self.client.get(reverse("join_event", args=[self.event.pk]), follow=True)
        self.assertContains(join_response, "You joined the event!")
        self.assertTrue(self.event.attendees.filter(pk=self.other_user.pk).exists())

        leave_response = self.client.get(reverse("leave_event", args=[self.event.pk]), follow=True)
        self.assertContains(leave_response, "You left the event.")
        self.assertFalse(self.event.attendees.filter(pk=self.other_user.pk).exists())


class EventBehaviorBDDTests(TestCase):
    """Behavior-focused tests written in Given/When/Then style."""

    def setUp(self):
        self.organizer = get_user_model().objects.create_user(username="charlie", password="secret123")
        self.attendee = get_user_model().objects.create_user(username="diana", password="secret123")
        self.event = Event.objects.create(
            title="Monthly Engineering Sync",
            description="Share progress and blockers.",
            date=timezone.now() + timedelta(days=5),
            location="Nairobi",
            organizer=self.organizer,
        )

    def test_given_guest_when_visiting_events_then_redirected_to_login(self):
        """Given a guest user, when opening events list, then they are redirected."""
        # Given: an unauthenticated visitor
        # When: they request the event list page
        response = self.client.get(reverse("event_list"))

        # Then: they are redirected to login
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_given_logged_in_user_when_creating_event_then_event_is_persisted(self):
        """Given an authenticated user, when posting valid event data, then event is saved."""
        # Given: a logged-in user and valid event payload
        self.client.force_login(self.organizer)
        payload = {
            "title": "BDD Demo Session",
            "description": "Show behavior-driven tests.",
            "date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M"),
            "location": "Kampala",
        }

        # When: the user submits the create-event form
        response = self.client.post(reverse("event_create"), payload, follow=True)

        # Then: success feedback is shown and event is stored
        self.assertContains(response, "Event created successfully!")
        self.assertTrue(Event.objects.filter(title="BDD Demo Session", organizer=self.organizer).exists())

    def test_given_non_attendee_when_joining_then_can_join_and_leave(self):
        """Given a user not attending, when joining then leaving, then attendee list updates."""
        # Given: another logged-in user who is not yet an attendee
        self.client.force_login(self.attendee)
        self.assertFalse(self.event.attendees.filter(pk=self.attendee.pk).exists())

        # When: the user joins the event
        join_response = self.client.get(reverse("join_event", args=[self.event.pk]), follow=True)

        # Then: they appear in attendees
        self.assertContains(join_response, "You joined the event!")
        self.assertTrue(self.event.attendees.filter(pk=self.attendee.pk).exists())

        # When: the same user leaves the event
        leave_response = self.client.get(reverse("leave_event", args=[self.event.pk]), follow=True)

        # Then: they are removed from attendees
        self.assertContains(leave_response, "You left the event.")
        self.assertFalse(self.event.attendees.filter(pk=self.attendee.pk).exists())
