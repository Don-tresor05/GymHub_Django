from django.db import models
from django.conf import settings

class Gym(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gym_images/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gyms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
