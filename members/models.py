from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid
from gymhub.constants import MembershipTiers

class MembershipPlan(models.Model):
    """Membership plans that gym owners can create for their gym"""
    DURATION_CHOICES = (
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', '3 Months'),
        ('SEMI_ANNUAL', '6 Months'),
        ('ANNUAL', 'Annual'),
    )
    
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='membership_plans')
    name = models.CharField(max_length=100, help_text="e.g., 'Basic Monthly', 'Premium Annual'")
    tier = models.CharField(max_length=20, choices=MembershipTiers.CHOICES, default=MembershipTiers.BASIC)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='MONTHLY')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in RWF")
    duration_days = models.IntegerField(default=30, help_text="Number of days this membership lasts")
    description = models.TextField(blank=True, help_text="Benefits and features included")
    is_active = models.BooleanField(default=True, help_text="Is this plan available for purchase?")
    max_family_members = models.IntegerField(default=1, help_text="For family plans, how many members allowed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['gym', 'price']
        unique_together = ['gym', 'name']
    
    def __str__(self):
        return f"{self.gym.name} - {self.name} ({self.price} RWF)"

class Membership(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('SUSPENDED', 'Suspended'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='members')
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='memberships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    joined_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    qr_code = models.CharField(max_length=100, unique=True, blank=True)
    
    # Family/Group membership
    is_family_plan = models.BooleanField(default=False)
    primary_member = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='family_members')

    def save(self, *args, **kwargs):
        # Generate QR code if not exists
        if not self.qr_code:
            self.qr_code = str(uuid.uuid4())
        
        # Set expiration date if not set (default 1 month)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)
        
        # Update status based on expiration
        if self.expires_at and timezone.now() > self.expires_at:
            self.status = 'EXPIRED'
            self.is_active = False
        
        super().save(*args, **kwargs)

    @property
    def membership_type(self):
        """Return membership type name for display"""
        if self.membership_plan:
            return self.membership_plan.name
        return "Basic Membership"
    
    def __str__(self):
        return f"{self.user.username} - {self.gym.name} ({self.membership_type})"
    
    class Meta:
        unique_together = ['user', 'gym']
