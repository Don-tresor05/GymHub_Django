from django import forms
from .models import GymClass, ClassBooking, ClassWaitlist

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
