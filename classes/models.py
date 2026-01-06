from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from gymhub.constants import ClassTypes, BookingStatus

class GymClass(models.Model):
    name = models.CharField(max_length=200)
    class_type = models.CharField(max_length=30, choices=ClassTypes.CHOICES, default=ClassTypes.YOGA)
    description = models.TextField(blank=True)
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='classes')
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_classes')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=20)
    is_recurring = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    
    def get_enrolled_count(self):
        return self.bookings.filter(status=BookingStatus.CONFIRMED).count()
    
    def get_available_spots(self):
        return self.capacity - self.get_enrolled_count()
    
    def is_full(self):
        return self.get_enrolled_count() >= self.capacity
    
    class Meta:
        verbose_name_plural = "Gym Classes"
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} at {self.gym.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"


class ClassBooking(models.Model):
    """Track member bookings for classes"""
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, related_name='bookings')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='class_bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BookingStatus.CHOICES, default=BookingStatus.CONFIRMED)
    
    def clean(self):
        # Check if class is full
        if self.gym_class.is_full() and self.status == BookingStatus.CONFIRMED:
            raise ValidationError('This class is full. Please join the waitlist.')
    
    def __str__(self):
        return f"{self.member.username} -> {self.gym_class.name}"
    
    class Meta:
        unique_together = ['gym_class', 'member']


class ClassWaitlist(models.Model):
    """Waitlist for full classes"""
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, related_name='waitlist')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waitlisted_classes')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_notified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.member.username} waiting for {self.gym_class.name}"
    
    class Meta:
        unique_together = ['gym_class', 'member']
        ordering = ['joined_at']
