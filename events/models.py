from datetime import timezone
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='events')

    def __str__(self):
        return self.name
    
    @property
    def is_upcoming(self):
        return self.date>=timezone.now().date()
    


class Participant(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    events = models.ManyToManyField(Event,related_name='participants')

    def __str__(self):
        return self.name
    