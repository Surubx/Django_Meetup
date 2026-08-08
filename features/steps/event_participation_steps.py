from behave import given, when, then
from datetime import timedelta
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from events.models import Event


class EventParticipationContext:
    def __init__(self):
        self.client = Client()
        self.organizer = None
        self.attendee = None
        self.event = None


context = EventParticipationContext()


def unique_username(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


@given('a guest user')
@given('a guest user is present')
def step_guest_user(context):
    context.client = Client()


@given('a logged-in user')
@given('a logged-in user is present')
def step_logged_in_user(context):
    context.organizer = get_user_model().objects.create_user(username=unique_username('charlie'), password='secret123')
    context.client = Client()
    context.client.force_login(context.organizer)


@given('a logged-in attendee')
@given('a logged-in attendee is present')
def step_logged_in_attendee(context):
    context.attendee = get_user_model().objects.create_user(username=unique_username('diana'), password='secret123')
    context.organizer = get_user_model().objects.create_user(username=unique_username('organizer'), password='secret123')
    context.event = Event.objects.create(
        title='Monthly Engineering Sync',
        description='Share progress and blockers.',
        date=timezone.now() + timedelta(days=5),
        location='Nairobi',
        organizer=context.organizer,
    )
    context.client = Client()
    context.client.force_login(context.attendee)


@given('a logged-in attendee who has joined an event')
@given('a logged-in attendee who has joined an event is present')
def step_logged_in_attendee_with_joined_event(context):
    context.attendee = get_user_model().objects.create_user(username=unique_username('eve'), password='secret123')
    context.organizer = get_user_model().objects.create_user(username=unique_username('organizer2'), password='secret123')
    context.event = Event.objects.create(
        title='Monthly Engineering Sync',
        description='Share progress and blockers.',
        date=timezone.now() + timedelta(days=5),
        location='Nairobi',
        organizer=context.organizer,
    )
    context.event.attendees.add(context.attendee)
    context.client = Client()
    context.client.force_login(context.attendee)


@when('the user visits the events page')
def step_visit_events_page(context):
    context.response = context.client.get(reverse('event_list'))


@when('the user creates a valid event')
def step_create_event(context):
    payload = {
        'title': 'BDD Demo Session',
        'description': 'Show behavior-driven tests.',
        'date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M'),
        'location': 'Kampala',
    }
    context.response = context.client.post(reverse('event_create'), payload, follow=True)


@when('the user joins an existing event')
def step_join_event(context):
    context.response = context.client.get(reverse('join_event', args=[context.event.pk]), follow=True)


@when('the user leaves the event')
def step_leave_event(context):
    context.response = context.client.get(reverse('leave_event', args=[context.event.pk]), follow=True)


@then('the user is redirected to login')
def step_redirected_to_login(context):
    assert context.response.status_code == 302
    assert '/login/' in context.response.url


@then('the event is saved successfully')
def step_event_saved(context):
    assert 'Event created successfully!' in context.response.content.decode()
    assert Event.objects.filter(title='BDD Demo Session', organizer=context.organizer).exists()


@then('the event shows the user as an attendee')
def step_event_shows_attendee(context):
    assert 'You joined the event!' in context.response.content.decode()
    assert context.event.attendees.filter(pk=context.attendee.pk).exists()


@then('the event no longer shows the user as an attendee')
def step_event_no_longer_shows_attendee(context):
    assert 'You left the event.' in context.response.content.decode()
    assert not context.event.attendees.filter(pk=context.attendee.pk).exists()
