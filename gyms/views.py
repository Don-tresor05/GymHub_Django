from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Gym
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
