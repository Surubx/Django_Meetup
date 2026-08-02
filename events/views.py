from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from .forms import SignUpForm, EventForm
from .models import Event

# Redirect the home page to the event list
def home(request):
    return redirect("event_list")

# Create a new user account
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("event_list")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


# Log in an existing user
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("event_list")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


# Log out the current user
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")

# Show all events on the main page
@login_required
def event_list(request):
    events = Event.objects.all().order_by("date")
    joined_event_ids = []
    if request.user.is_authenticated:
        joined_event_ids = list(request.user.joined_events.values_list("id", flat=True))
    return render(request, "events/event_list.html", {"events": events, "joined_event_ids": joined_event_ids})

# Create a new event
@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form, "title": "Create Event"})

# Edit an existing event if the current user created it
@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        messages.error(request, "You can only edit your own events.")
        return redirect("event_list")
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect("event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form, "title": "Edit Event"})

# Delete an event only if the current user created it
@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        messages.error(request, "You can only delete your own events.")
        return redirect("event_list")
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect("event_list")

# Add the current user to an event's attendee list
@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.attendees.add(request.user)
    messages.success(request, "You joined the event!")
    return redirect("event_list")

# Remove the current user from an event's attendee list
@login_required
def leave_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.attendees.remove(request.user)
    messages.success(request, "You left the event.")
    return redirect("event_list")

# Show events the current user joined
@login_required
def my_events(request):
    events = Event.objects.filter(attendees=request.user).order_by("date")
    return render(request, "events/my_events.html", {"events": events})

# Show upcoming events the user joined as reminders
@login_required
def reminder_view(request):
    upcoming = Event.objects.filter(attendees=request.user, date__gte=timezone.now()).order_by("date")
    return render(request, "events/reminders.html", {"upcoming": upcoming})
