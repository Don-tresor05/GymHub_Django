from django.db import models
from django.conf import settings
from django.utils import timezone

class Attendance(models.Model):
    """Track member check-ins and check-outs"""
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance_records')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='attendance_records')
    gym_class = models.ForeignKey('classes.GymClass', on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_records')
    
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    
    # QR code or manual check-in
    is_qr_checkin = models.BooleanField(default=False)
    checked_in_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_checkins')
    
    def get_duration(self):
        """Get session duration in minutes"""
        if self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            return int(delta.total_seconds() / 60)
        return None
    
    def __str__(self):
        return f"{self.member.username} at {self.gym.name} - {self.check_in_time.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-check_in_time']


class GuestPass(models.Model):
    """Track guest/visitor passes"""
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('USED', 'Used'),
        ('EXPIRED', 'Expired'),
    )
    
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='guest_passes')
    guest_name = models.CharField(max_length=200)
    guest_phone = models.CharField(max_length=15)
    guest_email = models.EmailField(blank=True)
    
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='issued_passes')
    issued_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    used_at = models.DateTimeField(null=True, blank=True)
    
    def is_valid(self):
        return self.status == 'ACTIVE' and timezone.now() < self.valid_until
    
    def __str__(self):
        return f"Guest Pass for {self.guest_name} at {self.gym.name}"
