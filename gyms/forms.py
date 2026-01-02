from django import forms
from .models import Gym

class GymUpdateForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ['name', 'address', 'contact_phone', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gym Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+250780000000'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell members about your gym...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
