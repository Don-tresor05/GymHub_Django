from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from gyms.models import Gym

class CustomUserCreationForm(UserCreationForm):
    gym_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not isinstance(self.fields[field].widget, forms.HiddenInput):
                self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': self.fields[field].label})

    def save(self, commit=True):
        user = super().save(commit=commit)
        gym_id = self.cleaned_data.get('gym_id')
        if commit and gym_id:
            try:
                from members.models import Membership
                from gyms.models import Gym
                gym = Gym.objects.get(pk=gym_id)
                Membership.objects.get_or_create(user=user, gym=gym)
            except Gym.DoesNotExist:
                pass
        return user

class GymOwnerRegistrationForm(CustomUserCreationForm):
    gym_name = forms.CharField(max_length=200, label="Gym Name")
    gym_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Gym Address")
    gym_phone = forms.CharField(max_length=15, label="Gym Contact Phone")
    gym_image = forms.ImageField(required=False, label="Gym Logo/Image")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].initial = 'GYM_OWNER'
        self.fields['role'].widget = forms.HiddenInput()
        # Add classes to gym specific fields as well (already handled by super().__init__ but let's be sure about the textarea rows)
        self.fields['gym_address'].widget.attrs.update({'rows': 3})

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.role = 'GYM_OWNER'
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
