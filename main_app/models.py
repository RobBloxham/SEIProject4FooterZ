from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Sneakers(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    colorway = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'sneakers_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    sneakers = models.ForeignKey(Sneakers, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for sneakers_id: {self.sneakers_id} @{self.url}"