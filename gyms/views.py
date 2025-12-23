from django.shortcuts import render, get_object_or_404
from .models import Gym

def gym_list(request):
    """View to list all gyms"""
    gyms = Gym.objects.all()
    return render(request, 'gyms/gym_list.html', {'gyms': gyms})

def gym_detail(request, pk):
    """View to show details of a specific gym"""
    gym = get_object_or_404(Gym, pk=pk)
    return render(request, 'gyms/gym_detail.html', {'gym': gym})
