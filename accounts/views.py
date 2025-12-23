from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, GymOwnerRegistrationForm

def home_view(request):
    """Home page view"""
    return render(request, 'home.html')

def register_view(request):
    """General User/Member registration view"""
    gym_id = request.GET.get('gym_id')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        initial_data = {}
        if gym_id:
            initial_data['gym_id'] = gym_id
        form = CustomUserCreationForm(initial=initial_data)
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Member Registration'})

def gym_owner_register_view(request):
    """Specialized Gym Owner registration view"""
    if request.method == 'POST':
        form = GymOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Gym and Owner account registered successfully!')
            return redirect('home')
    else:
        form = GymOwnerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Register Your Gym', 'is_gym_owner': True})

def profile_view(request):
    """User profile view"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'accounts/profile.html', {'user': request.user})