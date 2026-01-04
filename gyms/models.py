from django.db import models
from django.conf import settings

class Gym(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_phone = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gym_images/', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gyms')
    
    # Operating hours
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    
    # Pricing for membership tiers (in RWF)
    basic_price = models.DecimalField(max_digits=10, decimal_places=2, default=15000)
    premium_price = models.DecimalField(max_digits=10, decimal_places=2, default=25000)
    corporate_price = models.DecimalField(max_digits=10, decimal_places=2, default=20000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class GymFacility(models.Model):
    """Amenities and facilities available at a gym"""
    FACILITY_TYPES = (
        ('CARDIO', 'Cardio Equipment'),
        ('WEIGHTS', 'Weight Training'),
        ('POOL', 'Swimming Pool'),
        ('SAUNA', 'Sauna'),
        ('LOCKER', 'Locker Rooms'),
        ('SHOWER', 'Showers'),
        ('PARKING', 'Parking'),
        ('CAFE', 'Cafe'),
        ('OTHER', 'Other'),
    )
    
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='facilities')
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.gym.name} - {self.name}"
    
    class Meta:
        verbose_name_plural = "Gym Facilities"


class Equipment(models.Model):
    """Track gym equipment inventory and maintenance"""
    STATUS_CHOICES = (
        ('WORKING', 'Working'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('BROKEN', 'Broken'),
    )
    
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='equipment')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WORKING')
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.gym.name}"


class GymStaff(models.Model):
    """Link users to gyms with specific roles - allows gym owners to assign staff and trainers"""
    ROLE_CHOICES = (
        ('STAFF', 'Staff'),
        ('TRAINER', 'Trainer'),
        ('MANAGER', 'Manager'),
    )
    
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='gym_staff')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gym_assignments')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='staff_assignments_made')
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Permissions
    can_check_in_members = models.BooleanField(default=True)
    can_process_payments = models.BooleanField(default=True)
    can_manage_classes = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        # Update user's role when assigned
        if self.role == 'TRAINER' and self.user.role != 'TRAINER':
            self.user.role = 'TRAINER'
            self.user.save()
        elif self.role in ['STAFF', 'MANAGER'] and self.user.role not in ['STAFF', 'TRAINER', 'GYM_OWNER']:
            self.user.role = 'STAFF'
            self.user.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()} at {self.gym.name}"
    
    class Meta:
        unique_together = ['gym', 'user']
        verbose_name_plural = "Gym Staff"
