from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, GymOwnerRegistrationForm, UserUpdateForm

def home_view(request):
    """Home page view"""
    return render(request, 'home.html')

def register_view(request):
    """General User/Member registration view"""
    gym_id = request.GET.get('gym_id')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Check if they joined a gym during registration
            from members.models import Membership
            has_gym = Membership.objects.filter(user=user).exists()
            
            if has_gym:
                messages.success(request, 'Registration successful! Welcome to your gym!')
                return redirect('profile')
            else:
                messages.success(request, 'Registration successful! Now choose a gym to join.')
                return redirect('gym_list')
    else:
        initial_data = {}
        if gym_id:
            initial_data['gym_id'] = gym_id
        form = CustomUserCreationForm(initial=initial_data)
    
    context = {
        'form': form, 
        'title': 'Member Registration',
        'gym_id': gym_id  # Pass gym_id to template for display
    }
    return render(request, 'accounts/register.html', context)

def gym_owner_register_view(request):
    """Specialized Gym Owner registration view"""
    if request.method == 'POST':
        form = GymOwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Gym and Owner account registered successfully!')
            return redirect('home')
    else:
        form = GymOwnerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'title': 'Register Your Gym', 'is_gym_owner': True})

@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def join_gym_view(request, gym_id):
    """Allow existing members to join a gym"""
    from gyms.models import Gym
    from members.models import Membership
    
    if request.user.role != 'MEMBER':
        messages.error(request, 'Only members can join gyms.')
        return redirect('gym_detail', pk=gym_id)
    
    gym = get_object_or_404(Gym, pk=gym_id)
    
    # Check if already a member
    existing_membership = Membership.objects.filter(user=request.user, gym=gym).first()
    
    if existing_membership:
        if existing_membership.is_active:
            messages.info(request, f'You are already a member of {gym.name}!')
        else:
            existing_membership.is_active = True
            existing_membership.save()
            messages.success(request, f'Your membership to {gym.name} has been reactivated!')
    else:
        Membership.objects.create(user=request.user, gym=gym)
        messages.success(request, f'You have successfully joined {gym.name}!')
    
    return redirect('gym_detail', pk=gym_id)