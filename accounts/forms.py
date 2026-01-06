from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from gyms.models import Gym
from members.models import MembershipPlan
from gymhub.constants import UserRoles

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_photo', 
                  'emergency_contact_name', 'emergency_contact_phone', 'date_of_birth', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+250780000000'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency Contact Name'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+250780000000'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
        }

class UnifiedRegistrationForm(UserCreationForm):
    """Unified registration form for all user roles with approval workflow"""
    
    role = forms.ChoiceField(
        choices=[choice for choice in UserRoles.CHOICES if choice[0] != UserRoles.ADMIN],
        initial=UserRoles.MEMBER,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
        help_text="Select your role"
    )
    
    # For MEMBER role
    gym = forms.ModelChoiceField(
        queryset=Gym.objects.all(),
        required=False,
        empty_label="Select Your Gym",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_gym'}),
        help_text="Choose which gym you want to join (for members)"
    )
    
    membership_plan = forms.ModelChoiceField(
        queryset=MembershipPlan.objects.none(),
        required=False,
        empty_label="Select Membership Plan (Optional)",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_membership_plan'}),
        help_text="Choose your membership plan"
    )
    
    # For GYM_OWNER role
    gym_name = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Gym Name"
    )
    gym_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Gym Address"
    )
    gym_phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Gym Contact Phone"
    )
    registration_document = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Business Registration Document",
        help_text="Upload document proving gym ownership (PDF, JPG, PNG)"
    )
    
    # For STAFF/TRAINER role
    pending_gym = forms.ModelChoiceField(
        queryset=Gym.objects.all(),
        required=False,
        empty_label="Select Gym to Join",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_pending_gym'}),
        help_text="Choose which gym you want to work for"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2', 'role')

    def __init__(self, *args, exclude_roles=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter out excluded roles
        if exclude_roles:
            role_choices = [(key, value) for key, value in UserRoles.CHOICES if key not in exclude_roles]
            self.fields['role'].choices = role_choices
        
        for field in self.fields:
            if field not in ['gym', 'membership_plan', 'pending_gym', 'role', 'registration_document', 'gym_name', 'gym_address', 'gym_phone']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Dynamic membership plan loading
        if 'gym' in self.data:
            try:
                gym_id = int(self.data.get('gym'))
                self.fields['membership_plan'].queryset = MembershipPlan.objects.filter(gym_id=gym_id, is_active=True)
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        # Validate based on role
        if role == UserRoles.MEMBER:
            if not cleaned_data.get('gym'):
                self.add_error('gym', 'Please select a gym to join.')
        
        elif role == UserRoles.GYM_OWNER:
            if not cleaned_data.get('gym_name'):
                self.add_error('gym_name', 'Gym name is required for gym owners.')
            if not cleaned_data.get('gym_address'):
                self.add_error('gym_address', 'Gym address is required for gym owners.')
        
        elif role in [UserRoles.STAFF, UserRoles.TRAINER]:
            if not cleaned_data.get('pending_gym'):
                self.add_error('pending_gym', f'Please select a gym you want to work for as {role.lower()}.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        user.role = role
        
        # Set approval status based on role
        if role == UserRoles.MEMBER:
            user.is_approved = True  # Members are auto-approved
        else:
            user.is_approved = False  # GYM_OWNER, STAFF, TRAINER need approval
            user.is_active = False  # Disable account until approved
        
        # Handle document upload for gym owners
        if role == UserRoles.GYM_OWNER:
            user.registration_document = self.cleaned_data.get('registration_document')
        
        # Set pending gym for staff/trainers
        if role in [UserRoles.STAFF, UserRoles.TRAINER]:
            user.pending_gym = self.cleaned_data.get('pending_gym')
        
        if commit:
            user.save()
            
            # Create gym for gym owners (pending approval)
            if role == UserRoles.GYM_OWNER:
                Gym.objects.create(
                    name=self.cleaned_data['gym_name'],
                    address=self.cleaned_data['gym_address'],
                    contact_phone=self.cleaned_data.get('gym_phone', ''),
                    owner=user
                )
            
            # Create membership for members
            elif role == UserRoles.MEMBER:
                from members.models import Membership
                from datetime import timedelta
                from django.utils import timezone
                
                gym = self.cleaned_data.get('gym')
                membership_plan = self.cleaned_data.get('membership_plan')
                
                if gym:
                    membership_data = {'user': user, 'gym': gym}
                    
                    if membership_plan:
                        membership_data['membership_plan'] = membership_plan
                        membership_data['expires_at'] = timezone.now() + timedelta(days=membership_plan.duration_days)
                    
                    Membership.objects.create(**membership_data)
        
        return user

# Keep old form for backward compatibility
CustomUserCreationForm = UnifiedRegistrationForm

class GymOwnerRegistrationForm(CustomUserCreationForm):
    gym_name = forms.CharField(max_length=200, label="Gym Name")
    gym_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Gym Address")
    gym_phone = forms.CharField(max_length=15, label="Gym Contact Phone")
    gym_image = forms.ImageField(required=False, label="Gym Logo/Image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add classes to gym specific fields as well
        self.fields['gym_address'].widget.attrs.update({'rows': 3})
        # Hide gym and membership_plan fields for gym owner registration
        if 'gym' in self.fields:
            self.fields['gym'].widget = forms.HiddenInput()
            self.fields['gym'].required = False
        if 'membership_plan' in self.fields:
            self.fields['membership_plan'].widget = forms.HiddenInput()
            self.fields['membership_plan'].required = False

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.role = UserRoles.GYM_OWNER
        if commit:
            user.save()
            Gym.objects.create(
                name=self.cleaned_data['gym_name'],
                address=self.cleaned_data['gym_address'],
                contact_phone=self.cleaned_data['gym_phone'],
                image=self.cleaned_data.get('gym_image'),
                owner=user
            )
        return user
