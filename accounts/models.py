from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('MEMBER', 'Member'),
        ('TRAINER', 'Trainer'),
        ('GYM_OWNER', 'Gym Owner'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
