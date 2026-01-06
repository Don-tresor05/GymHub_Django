from django.contrib.auth.models import AbstractUser
from django.db import models
from gymhub.constants import UserRoles

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=UserRoles.CHOICES, default=UserRoles.MEMBER)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    
    # Approval workflow fields
    is_approved = models.BooleanField(default=True, help_text="Admin/Owner approval status")
    registration_document = models.FileField(
        upload_to='registration_documents/', 
        blank=True, 
        null=True,
        help_text="Document proving gym ownership (for gym owners only)"
    )
    pending_gym = models.ForeignKey(
        'gyms.Gym', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='pending_staff',
        help_text="Gym where staff/trainer is requesting access"
    )
    approved_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_users',
        help_text="Admin or gym owner who approved this user"
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, help_text="Reason for rejection if applicable")
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def needs_approval(self):
        """Check if user needs approval based on role"""
        return self.role in ['GYM_OWNER', 'STAFF', 'TRAINER'] and not self.is_approved
