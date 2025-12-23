from django.db import models
from django.conf import settings

class Membership(models.Model):
    TIER_CHOICES = (
        ('BASIC', 'Basic'),
        ('PREMIUM', 'Premium'),
        ('CORPORATE', 'Corporate'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='members')
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='BASIC')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.gym.name} ({self.tier})"
