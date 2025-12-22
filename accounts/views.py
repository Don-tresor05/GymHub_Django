from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home_view(request):
    """Home page view"""
    return render(request, 'home.html')

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def profile_view(request):
    """User profile view"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'accounts/profile.html', {'user': request.user})