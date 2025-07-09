from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')

    # RSVP ManyToMany to User with related_name for reverse access
    rsvps = models.ManyToManyField(User, related_name='rsvp_events', blank=True)

    # Image field with default image (ensure file exists in media)
    image = models.ImageField(upload_to='event_images/', default='event_images/default.jpg', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # track creation
    updated_at = models.DateTimeField(auto_now=True)      # track last update

    def __str__(self):
        return self.name

    @property
    def is_upcoming(self):
        # Checks if event date is today or in future
        return self.date >= timezone.now().date()

    class Meta:
        ordering = ['-date', '-time']  # newest events first
