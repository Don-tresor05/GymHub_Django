from django.db import models
from django.conf import settings

class GymClass(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='classes')
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_classes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=20)
    
    class Meta:
        verbose_name_plural = "Gym Classes"

    def __str__(self):
        return f"{self.name} at {self.gym.name}"
