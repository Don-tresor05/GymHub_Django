from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from gyms.models import Gym

class CustomUserCreationForm(UserCreationForm):
    gym_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'role')

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
    gym_address = forms.CharField(widget=forms.Textarea, label="Gym Address")
    gym_phone = forms.CharField(max_length=15, label="Gym Contact Phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].initial = 'GYM_OWNER'
        self.fields['role'].widget = forms.HiddenInput()

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.role = 'GYM_OWNER'
        if commit:
            user.save()
            Gym.objects.create(
                name=self.cleaned_data['gym_name'],
                address=self.cleaned_data['gym_address'],
                contact_phone=self.cleaned_data['gym_phone'],
                owner=user
            )
        return user
