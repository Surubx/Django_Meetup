from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    attendees = models.ManyToManyField(User, related_name="joined_events", blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
