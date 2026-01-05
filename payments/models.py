from django.db import models
from django.conf import settings
import uuid

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )
    
    PAYMENT_METHOD = (
        ('CASH', 'Cash'),
        ('MTN_MOMO', 'MTN Mobile Money'),
        ('AIRTEL_MONEY', 'Airtel Money'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CARD', 'Card'),
    )
    
    PAYMENT_TYPE = (
        ('MEMBERSHIP', 'Membership Fee'),
        ('CLASS', 'Class Fee'),
        ('PERSONAL_TRAINING', 'Personal Training'),
        ('OTHER', 'Other'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name='payments')
    membership = models.ForeignKey('members.Membership', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='CASH')
    payment_type = models.CharField(max_length=30, choices=PAYMENT_TYPE, default='MEMBERSHIP')
    
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    mobile_money_number = models.CharField(max_length=15, blank=True)
    
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)
    
    description = models.TextField(blank=True)
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_payments')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Generate transaction ID if not exists
        if not self.transaction_id:
            self.transaction_id = str(uuid.uuid4())
        
        # Generate receipt number if payment is completed
        if self.status == 'COMPLETED' and not self.receipt_number:
            self.receipt_number = f"GH-{self.created_at.strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.amount} RWF ({self.status})"
