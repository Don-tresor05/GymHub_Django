from django import forms
from .models import Payment
from accounts.models import User
from members.models import Membership

class PaymentForm(forms.ModelForm):
    """Form for staff to process payments"""
    
    class Meta:
        model = Payment
        fields = ['user', 'amount', 'payment_method', 'payment_type', 'membership', 'mobile_money_number', 'description']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
            'membership': forms.Select(attrs={'class': 'form-select'}),
            'mobile_money_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '078XXXXXXX'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Payment notes...'}),
        }
    
    def __init__(self, *args, **kwargs):
        gym = kwargs.pop('gym', None)
        super().__init__(*args, **kwargs)
        
        if gym:
            # Filter users to only members of this gym
            self.fields['user'].queryset = User.objects.filter(
                memberships__gym=gym,
                memberships__is_active=True
            ).distinct()
            
            # Filter memberships to only this gym
            self.fields['membership'].queryset = Membership.objects.filter(
                gym=gym
            )
        
        # Make mobile money number optional
        self.fields['mobile_money_number'].required = False
        self.fields['membership'].required = False
        self.fields['description'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        mobile_money_number = cleaned_data.get('mobile_money_number')
        
        # Validate mobile money number for mobile money payments
        if payment_method in ['MTN_MOMO', 'AIRTEL_MONEY']:
            if not mobile_money_number:
                raise forms.ValidationError("Mobile money number is required for mobile money payments.")
            
            # Basic Rwanda phone number validation
            if not mobile_money_number.startswith('07') or len(mobile_money_number) != 10:
                raise forms.ValidationError("Invalid Rwandan phone number. Must be 10 digits starting with 07.")
        
        return cleaned_data
