from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event


class EventParticipationSteps(TestCase):
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

    def test_guest_user_visits_the_events_page(self):
        response = self.client.get(reverse("event_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_logged_in_user_creates_a_valid_event(self):
        self.client.force_login(self.organizer)
        payload = {
            "title": "BDD Demo Session",
            "description": "Show behavior-driven tests.",
            "date": (timezone.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M"),
            "location": "Kampala",
        }
        response = self.client.post(reverse("event_create"), payload, follow=True)
        self.assertContains(response, "Event created successfully!")
        self.assertTrue(Event.objects.filter(title="BDD Demo Session", organizer=self.organizer).exists())

    def test_non_attendee_joins_and_leaves_the_event(self):
        self.client.force_login(self.attendee)
        self.assertFalse(self.event.attendees.filter(pk=self.attendee.pk).exists())

        join_response = self.client.get(reverse("join_event", args=[self.event.pk]), follow=True)
        self.assertContains(join_response, "You joined the event!")
        self.assertTrue(self.event.attendees.filter(pk=self.attendee.pk).exists())

        leave_response = self.client.get(reverse("leave_event", args=[self.event.pk]), follow=True)
        self.assertContains(leave_response, "You left the event.")
        self.assertFalse(self.event.attendees.filter(pk=self.attendee.pk).exists())
