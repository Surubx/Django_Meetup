from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Model for a meetup or event
class Event(models.Model):


    def __str__(self):
        return self.title
