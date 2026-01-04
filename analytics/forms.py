from django import forms
from .models import Attendance
from accounts.models import User
from gyms.models import Gym
from classes.models import GymClass

class CheckInForm(forms.ModelForm):
    """Form for staff to check in members"""
    member = forms.ModelChoiceField(
        queryset=User.objects.filter(role='MEMBER'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Member"
    )
    gym_class = forms.ModelChoiceField(
        queryset=GymClass.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Class (Optional)",
        empty_label="General Gym Use"
    )
    
    class Meta:
        model = Attendance
        fields = ['member', 'gym_class']
    
    def __init__(self, *args, gym=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.gym = gym
        
        if gym:
            # Only show members of this gym
            from members.models import Membership
            member_ids = Membership.objects.filter(gym=gym, is_active=True).values_list('user_id', flat=True)
            self.fields['member'].queryset = User.objects.filter(id__in=member_ids, role='MEMBER')
            
            # Only show upcoming classes at this gym
            from django.utils import timezone
            self.fields['gym_class'].queryset = GymClass.objects.filter(
                gym=gym,
                start_time__date=timezone.now().date()
            ).order_by('start_time')

class QRCheckInForm(forms.Form):
    """Form for QR code check-in"""
    qr_code = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Scan QR Code',
            'autofocus': True
        }),
        label="Member QR Code"
    )
