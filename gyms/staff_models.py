from django.db import models
from django.conf import settings

class StaffAssignment(models.Model):
    """Model to track staff assignments to gyms"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_assignments')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='staff_members')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('user', 'gym')
    
    def __str__(self):
        return f"{self.user.username} - Staff at {self.gym.name}"
