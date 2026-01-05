from django import forms
from .models import GymClass, ClassBooking, ClassWaitlist
from gyms.models import Gym
from accounts.models import User

class ClassBookingForm(forms.ModelForm):
    """Form for members to book a class"""
    class Meta:
        model = ClassBooking
        fields = []  # No fields needed, just confirmation
    
    def __init__(self, *args, gym_class=None, member=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.gym_class = gym_class
        self.member = member
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if already booked
        if ClassBooking.objects.filter(gym_class=self.gym_class, member=self.member).exists():
            raise forms.ValidationError('You have already booked this class.')
        
        # Check if class is full
        if self.gym_class.is_full():
            raise forms.ValidationError('This class is full. Please join the waitlist.')
        
        return cleaned_data
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.gym_class = self.gym_class
        booking.member = self.member
        if commit:
            booking.save()
        return booking

class ClassForm(forms.ModelForm):
    """Form for owners/staff/trainers to create a class"""
    gym = forms.ModelChoiceField(queryset=Gym.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    trainer = forms.ModelChoiceField(queryset=User.objects.filter(role='TRAINER'), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = GymClass
        fields = ['name', 'class_type', 'description', 'gym', 'trainer', 'start_time', 'end_time', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'class_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit gyms and trainers based on role
        if user is not None:
            from gyms.models import GymStaff
            if getattr(user, 'role', None) == 'GYM_OWNER':
                self.fields['gym'].queryset = Gym.objects.filter(owner=user)
                trainer_user_ids = GymStaff.objects.filter(gym__owner=user, role='TRAINER', is_active=True).values_list('user_id', flat=True)
                self.fields['trainer'].queryset = User.objects.filter(id__in=trainer_user_ids)
            elif getattr(user, 'role', None) == 'TRAINER':
                gym_ids = GymStaff.objects.filter(user=user, role='TRAINER', is_active=True).values_list('gym_id', flat=True)
                self.fields['gym'].queryset = Gym.objects.filter(id__in=gym_ids)
                # Trainer creating class defaults to self
                self.fields['trainer'].queryset = User.objects.filter(id=user.id)
                self.fields['trainer'].initial = user
            elif getattr(user, 'role', None) == 'STAFF':
                gym_ids = GymStaff.objects.filter(user=user, is_active=True).values_list('gym_id', flat=True)
                self.fields['gym'].queryset = Gym.objects.filter(id__in=gym_ids)
                trainer_user_ids = GymStaff.objects.filter(gym_id__in=gym_ids, role='TRAINER', is_active=True).values_list('user_id', flat=True)
                self.fields['trainer'].queryset = User.objects.filter(id__in=trainer_user_ids)

