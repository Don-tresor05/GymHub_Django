from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import GymClass, ClassBooking, ClassWaitlist
from .forms import ClassBookingForm
from members.models import Membership

def class_list(request):
    """View to list all classes"""
    # Filter for upcoming classes
    upcoming_classes = GymClass.objects.filter(
        start_time__gte=timezone.now(),
        is_cancelled=False
    ).select_related('gym', 'trainer').order_by('start_time')
    
    # Filter by gym if specified
    gym_id = request.GET.get('gym')
    if gym_id:
        upcoming_classes = upcoming_classes.filter(gym_id=gym_id)
    
    context = {
        'classes': upcoming_classes,
        'title': 'Available Classes'
    }
    
    return render(request, 'classes/class_list.html', context)

@login_required
def class_detail(request, pk):
    """View class details"""
    gym_class = get_object_or_404(GymClass, pk=pk)
    
    # Check if user has booked this class
    user_booking = None
    user_in_waitlist = False
    can_book = False
    
    if request.user.role == 'MEMBER':
        user_booking = ClassBooking.objects.filter(gym_class=gym_class, member=request.user).first()
        user_in_waitlist = ClassWaitlist.objects.filter(gym_class=gym_class, member=request.user).exists()
        
        # Check if user is a member of this gym
        membership = Membership.objects.filter(user=request.user, gym=gym_class.gym, is_active=True).first()
        can_book = membership is not None and not user_booking and not user_in_waitlist
    
    context = {
        'gym_class': gym_class,
        'user_booking': user_booking,
        'user_in_waitlist': user_in_waitlist,
        'can_book': can_book,
        'title': gym_class.name
    }
    
    return render(request, 'classes/class_detail.html', context)

@login_required
def book_class(request, pk):
    """Book a class"""
    if request.user.role != 'MEMBER':
        messages.error(request, 'Only members can book classes.')
        return redirect('class_list')
    
    gym_class = get_object_or_404(GymClass, pk=pk)
    
    # Check if user is a member of this gym
    membership = Membership.objects.filter(user=request.user, gym=gym_class.gym, is_active=True).first()
    
    if not membership:
        messages.error(request, 'You must be a member of this gym to book classes.')
        return redirect('class_detail', pk=pk)
    
    # Check if already booked
    if ClassBooking.objects.filter(gym_class=gym_class, member=request.user).exists():
        messages.warning(request, 'You have already booked this class.')
        return redirect('class_detail', pk=pk)
    
    # Check if class is full
    if gym_class.is_full():
        messages.warning(request, 'This class is full. You have been added to the waitlist.')
        ClassWaitlist.objects.get_or_create(gym_class=gym_class, member=request.user)
        return redirect('class_detail', pk=pk)
    
    # Create booking
    ClassBooking.objects.create(
        gym_class=gym_class,
        member=request.user,
        status='CONFIRMED'
    )
    
    messages.success(request, f'Successfully booked {gym_class.name}!')
    return redirect('my_bookings')

@login_required
def cancel_booking(request, pk):
    """Cancel a class booking"""
    booking = get_object_or_404(ClassBooking, pk=pk, member=request.user)
    
    gym_class = booking.gym_class
    booking.status = 'CANCELLED'
    booking.save()
    
    # Check if anyone is waiting
    waitlist_entry = ClassWaitlist.objects.filter(gym_class=gym_class, is_notified=False).first()
    if waitlist_entry:
        # Notify first person in waitlist (could send email here)
        waitlist_entry.is_notified = True
        waitlist_entry.save()
        messages.info(request, 'A spot has opened up and the first person on the waitlist has been notified.')
    
    messages.success(request, f'Booking for {gym_class.name} has been cancelled.')
    return redirect('my_bookings')

@login_required
def my_bookings(request):
    """View user's class bookings"""
    if request.user.role != 'MEMBER':
        messages.error(request, 'Only members can view bookings.')
        return redirect('home')
    
    # Get upcoming bookings
    upcoming_bookings = ClassBooking.objects.filter(
        member=request.user,
        gym_class__start_time__gte=timezone.now(),
        status='CONFIRMED'
    ).select_related('gym_class', 'gym_class__gym', 'gym_class__trainer').order_by('gym_class__start_time')
    
    # Get past bookings
    past_bookings = ClassBooking.objects.filter(
        member=request.user,
        gym_class__start_time__lt=timezone.now()
    ).select_related('gym_class', 'gym_class__gym').order_by('-gym_class__start_time')[:10]
    
    # Get waitlist entries
    waitlist = ClassWaitlist.objects.filter(
        member=request.user,
        gym_class__start_time__gte=timezone.now()
    ).select_related('gym_class', 'gym_class__gym').order_by('gym_class__start_time')
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'waitlist': waitlist,
        'title': 'My Class Bookings'
    }
    
    return render(request, 'classes/my_bookings.html', context)

