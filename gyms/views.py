from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.contrib import messages
from .models import Gym
from .forms import GymUpdateForm
from members.models import Membership
from payments.models import Payment
from classes.models import GymClass
from django.utils import timezone

def gym_list(request):
    """View to list all gyms"""
    gyms = Gym.objects.all()
    return render(request, 'gyms/gym_list.html', {'gyms': gyms})

def gym_detail(request, pk):
    """View to show details of a specific gym"""
    gym = get_object_or_404(Gym, pk=pk)
    return render(request, 'gyms/gym_detail.html', {'gym': gym})

@login_required
def gym_owner_dashboard(request):
    """Dashboard view for Gym Owners"""
    if request.user.role != 'GYM_OWNER':
        return redirect('home')
    
    # Get the owner's primary gym (assuming one for now, or use list)
    my_gyms = Gym.objects.filter(owner=request.user)
    
    # Total Members across all owned gyms
    total_members = Membership.objects.filter(gym__in=my_gyms, is_active=True).count()
    
    # Total Revenue (Completed payments)
    total_revenue = Payment.objects.filter(gym__in=my_gyms, status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Upcoming Classes
    upcoming_classes = GymClass.objects.filter(gym__in=my_gyms, start_time__gte=timezone.now()).order_by('start_time')[:5]
    
    context = {
        'gyms': my_gyms,
        'total_members': total_members,
        'total_revenue': total_revenue,
        'upcoming_classes': upcoming_classes,
        'title': 'Gym Owner Dashboard'
    }
    
    return render(request, 'gyms/dashboard.html', context)

@login_required
def gym_detail_owner(request, pk):
    """Gym detail view for gym owner"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    
    # Get stats for this gym
    total_members = Membership.objects.filter(gym=gym, is_active=True).count()
    total_revenue = Payment.objects.filter(gym=gym, status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0
    upcoming_classes = GymClass.objects.filter(gym=gym, start_time__gte=timezone.now()).order_by('start_time')[:5]
    
    context = {
        'gym': gym,
        'total_members': total_members,
        'total_revenue': total_revenue,
        'upcoming_classes': upcoming_classes,
    }
    
    return render(request, 'gyms/gym_detail_owner.html', context)

@login_required
def gym_edit(request, pk):
    """Edit gym details"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = GymUpdateForm(request.POST, request.FILES, instance=gym)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gym details updated successfully!')
            return redirect('gym_detail_owner', pk=gym.pk)
    else:
        form = GymUpdateForm(instance=gym)
    
    return render(request, 'gyms/gym_edit.html', {'form': form, 'gym': gym})
