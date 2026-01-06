from django.db import models
from django.conf import settings

class TrainerProfile(models.Model):
    """Extended profile for trainers - optional additional info"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trainer_profile')
    specialties = models.TextField(blank=True, help_text="E.g., Yoga, Aerobics, Weight Training, Traditional Dance")
    bio = models.TextField(blank=True)
    certifications = models.TextField(blank=True, help_text="List certifications, one per line")
    years_experience = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_freelance = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Trainer Profile"


class TrainerAvailability(models.Model):
    """Track trainer weekly schedule"""
    DAYS_OF_WEEK = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='availability')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.trainer.user.username} - {self.get_day_of_week_display()}"
    
    class Meta:
        verbose_name_plural = "Trainer Availabilities"


class ClientAssignment(models.Model):
    """Assign clients to trainers for personal training"""
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='clients')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_trainers')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.trainer.user.username} -> {self.member.username}"


class TrainerCommission(models.Model):
    """Track trainer earnings from sessions"""
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE, related_name='commissions')
    session_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.trainer.user.username} - {self.amount} RWF"
