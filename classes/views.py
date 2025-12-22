from django.shortcuts import render

def class_list(request):
    """View to list all classes"""
    return render(request, 'classes/class_list.html')
