from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, date
from classes.models import GymClass, ClassBooking
from gyms.models import GymStaff

@login_required
def trainer_dashboard(request):
    if request.user.role != 'TRAINER':
        if request.user.role == 'GYM_OWNER':
            return redirect('gym_owner_dashboard')
        elif request.user.role == 'STAFF':
            return redirect('staff_dashboard')
        else:
            return redirect('member_dashboard')
    today = timezone.localdate()
    upcoming_classes = GymClass.objects.filter(
        trainer=request.user,
        is_cancelled=False,
        start_time__date__gte=today
    ).order_by('start_time')[:10]
    recent_classes = GymClass.objects.filter(
        trainer=request.user,
        start_time__date__lt=today
    ).order_by('-start_time')[:10]

    # Staff assignment and permissions (if trainer is also assigned as staff)
    staff_assignment = GymStaff.objects.filter(user=request.user, role='TRAINER', is_active=True).select_related('gym').first()
    
    context = {
        'title': 'Trainer Dashboard',
        'upcoming_classes': upcoming_classes,
        'recent_classes': recent_classes,
        'staff_assignment': staff_assignment,
    }
    return render(request, 'accounts/trainer_dashboard.html', context)

@login_required
def manage_availability(request):
    if request.user.role != 'TRAINER':
        return redirect('home')
    upcoming_classes = GymClass.objects.filter(trainer=request.user, start_time__gte=timezone.now()).order_by('start_time')
    return render(request, 'trainers/availability.html', {
        'title': 'Manage Availability',
        'upcoming_classes': upcoming_classes,
    })

@login_required
def manage_clients(request):
    if request.user.role != 'TRAINER':
        return redirect('home')
    bookings = ClassBooking.objects.filter(gym_class__trainer=request.user).select_related('member', 'gym_class').order_by('-booked_at')
    # Unique clients
    client_ids = set(bookings.values_list('member_id', flat=True))
    return render(request, 'trainers/clients.html', {
        'title': 'Manage Clients',
        'bookings': bookings,
        'client_count': len(client_ids),
    })

@login_required
def performance_analytics(request):
    if request.user.role != 'TRAINER':
        return redirect('home')
    start_date = date.today() - timedelta(days=30)
    recent_bookings = ClassBooking.objects.filter(gym_class__trainer=request.user, booked_at__date__gte=start_date)
    total_confirmed = recent_bookings.filter(status='CONFIRMED').count()
    total_cancelled = recent_bookings.filter(status='CANCELLED').count()
    total_classes = GymClass.objects.filter(trainer=request.user, start_time__date__gte=start_date).count()
    return render(request, 'trainers/performance.html', {
        'title': 'Performance Analytics',
        'total_confirmed': total_confirmed,
        'total_cancelled': total_cancelled,
        'total_classes': total_classes,
    })

@login_required
def earnings_summary(request):
    if request.user.role != 'TRAINER':
        return redirect('home')
    # Placeholder: integrate class/session payments later
    total_earnings = 0
    return render(request, 'trainers/earnings.html', {
        'title': 'Commission & Earnings',
        'total_earnings': total_earnings,
    })
