from django.shortcuts import render

def gym_list(request):
    """View to list all gyms"""
    return render(request, 'gyms/gym_list.html')
