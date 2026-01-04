from django import forms
from .models import GymFacility, Equipment

class GymFacilityForm(forms.ModelForm):
    """Form for adding/editing gym facilities"""
    
    class Meta:
        model = GymFacility
        fields = ['name', 'facility_type', 'description', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Main Swimming Pool'}),
            'facility_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Facility details...'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EquipmentForm(forms.ModelForm):
    """Form for adding/editing gym equipment"""
    
    class Meta:
        model = Equipment
        fields = ['name', 'brand', 'purchase_date', 'status', 'last_maintenance', 'next_maintenance', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Treadmill Pro 3000'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Life Fitness'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'last_maintenance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_maintenance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Equipment notes...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].required = False
        self.fields['purchase_date'].required = False
        self.fields['last_maintenance'].required = False
        self.fields['next_maintenance'].required = False
        self.fields['notes'].required = False
