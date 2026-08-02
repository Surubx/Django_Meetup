from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Model for a meetup or event
class Event(models.Model):
    title = models.CharField(max_length=200)  # Event name
    description = models.TextField()  # Event details
    date = models.DateTimeField()  # When the event happens
    location = models.CharField(max_length=200)  # Where the event happens
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    attendees = models.ManyToManyField(User, related_name="joined_events", blank=True)
    created_at = models.DateTimeField(default=timezone.now)  # When the event was created

    def __str__(self):
        return self.title
