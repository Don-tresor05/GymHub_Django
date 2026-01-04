from django import forms
from .models import Gym, GymStaff
from accounts.models import User
from members.models import MembershipPlan

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


class MembershipPlanForm(forms.ModelForm):
    """Form for gym owners to create membership plans"""
    class Meta:
        model = MembershipPlan
        fields = ['name', 'tier', 'duration', 'price', 'duration_days', 'description', 'is_active', 'max_family_members']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Basic Monthly'}),
            'tier': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in RWF', 'step': '1000'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30 for monthly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List benefits and features...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_family_members': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1 for individual, 4+ for family'}),
        }


class AssignStaffForm(forms.ModelForm):
    """Form for gym owners to assign staff/trainers to their gym"""
    user_email = forms.EmailField(
        label="User Email",
        help_text="Enter the email of the user you want to assign",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@example.com'})
    )
    
    class Meta:
        model = GymStaff
        fields = ['role', 'can_check_in_members', 'can_process_payments', 'can_manage_classes', 'can_view_reports']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'can_check_in_members': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_process_payments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_classes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_view_reports': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.gym = kwargs.pop('gym', None)
        super().__init__(*args, **kwargs)
        
        # Set default permissions based on role
        if not self.instance.pk:
            self.fields['can_check_in_members'].initial = True
            self.fields['can_process_payments'].initial = True
    
    def clean_user_email(self):
        email = self.cleaned_data.get('user_email')
        try:
            user = User.objects.get(email=email)
            
            # Check if user is already assigned to this gym
            if self.gym and GymStaff.objects.filter(gym=self.gym, user=user).exists():
                raise forms.ValidationError('This user is already assigned to your gym.')
            
            # Don't allow assigning gym owners
            if user.role == 'GYM_OWNER':
                raise forms.ValidationError('Cannot assign gym owners as staff.')
            
            return user
        except User.DoesNotExist:
            raise forms.ValidationError('No user found with this email address.')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user_email']
        
        if commit:
            instance.save()
        
        return instance


class UpdateStaffPermissionsForm(forms.ModelForm):
    """Form to update staff permissions"""
    class Meta:
        model = GymStaff
        fields = ['role', 'is_active', 'can_check_in_members', 'can_process_payments', 'can_manage_classes', 'can_view_reports']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_check_in_members': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_process_payments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_classes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_view_reports': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
