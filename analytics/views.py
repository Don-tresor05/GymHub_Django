from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Sum, Avg
from django.db.models.functions import TruncDate, TruncMonth
from datetime import timedelta, date
from .models import Attendance
from .forms import CheckInForm, QRCheckInForm
from gyms.models import Gym, GymStaff
from accounts.models import User
from payments.models import Payment
from members.models import Membership
import json

@login_required
def check_in_dashboard(request):
    """Dashboard for staff to manage check-ins"""
    if request.user.role != 'STAFF':
        messages.error(request, 'Only staff can access check-in system.')
        return redirect('home')
    
    # Get staff assignment
    staff_assignment = GymStaff.objects.filter(user=request.user).first()
    
    if not staff_assignment or not staff_assignment.can_check_in_members:
        messages.error(request, 'You do not have permission to check in members.')
        return redirect('staff_dashboard')
    
    gym = staff_assignment.gym
    
    # Get today's check-ins
    from datetime import date
    today_checkins = Attendance.objects.filter(
        gym=gym,
        check_in_time__date=date.today()
    ).select_related('member', 'gym_class').order_by('-check_in_time')
    
    # Get currently checked-in members (no checkout yet)
    active_checkins = today_checkins.filter(check_out_time__isnull=True)
    
    context = {
        'gym': gym,
        'today_checkins': today_checkins[:20],
        'active_checkins': active_checkins,
        'total_today': today_checkins.count(),
        'currently_in_gym': active_checkins.count(),
        'title': 'Check-In Dashboard'
    }
    
    return render(request, 'analytics/check_in_dashboard.html', context)

@login_required
def manual_check_in(request):
    """Manual check-in for members"""
    if request.user.role != 'STAFF':
        messages.error(request, 'Only staff can check in members.')
        return redirect('home')
    
    staff_assignment = GymStaff.objects.filter(user=request.user).first()
    
    if not staff_assignment or not staff_assignment.can_check_in_members:
        messages.error(request, 'You do not have permission to check in members.')
        return redirect('staff_dashboard')
    
    gym = staff_assignment.gym
    
    if request.method == 'POST':
        form = CheckInForm(request.POST, gym=gym)
        if form.is_valid():
            member = form.cleaned_data['member']
            
            # Check if already checked in today
            existing_checkin = Attendance.objects.filter(
                member=member,
                gym=gym,
                check_out_time__isnull=True
            ).first()
            
            if existing_checkin:
                messages.warning(request, f'{member.username} is already checked in!')
                return redirect('check_in_dashboard')
            
            # Create check-in
            attendance = form.save(commit=False)
            attendance.gym = gym
            attendance.is_qr_checkin = False
            attendance.checked_in_by = request.user
            attendance.save()
            
            messages.success(request, f'{member.username} checked in successfully!')
            return redirect('check_in_dashboard')
    else:
        form = CheckInForm(gym=gym)
    
    context = {
        'form': form,
        'gym': gym,
        'title': 'Manual Check-In'
    }
    
    return render(request, 'analytics/manual_check_in.html', context)

@login_required
def qr_check_in(request):
    """QR code check-in"""
    if request.user.role != 'STAFF':
        messages.error(request, 'Only staff can process QR check-ins.')
        return redirect('home')
    
    staff_assignment = GymStaff.objects.filter(user=request.user).first()
    
    if not staff_assignment or not staff_assignment.can_check_in_members:
        messages.error(request, 'You do not have permission to check in members.')
        return redirect('staff_dashboard')
    
    gym = staff_assignment.gym
    
    if request.method == 'POST':
        form = QRCheckInForm(request.POST)
        if form.is_valid():
            qr_code = form.cleaned_data['qr_code']
            
            # QR code format: GYMHUB-{user_id}
            try:
                if qr_code.startswith('GYMHUB-'):
                    user_id = int(qr_code.split('-')[1])
                    member = User.objects.get(id=user_id, role='MEMBER')
                    
                    # Verify member belongs to this gym
                    from members.models import Membership
                    membership = Membership.objects.filter(user=member, gym=gym, is_active=True).first()
                    
                    if not membership:
                        messages.error(request, f'{member.username} is not a member of {gym.name}!')
                        return redirect('qr_check_in')
                    
                    # Check if already checked in
                    existing_checkin = Attendance.objects.filter(
                        member=member,
                        gym=gym,
                        check_out_time__isnull=True
                    ).first()
                    
                    if existing_checkin:
                        messages.warning(request, f'{member.username} is already checked in!')
                    else:
                        # Create check-in
                        Attendance.objects.create(
                            member=member,
                            gym=gym,
                            is_qr_checkin=True,
                            checked_in_by=request.user
                        )
                        messages.success(request, f'{member.username} checked in successfully via QR!')
                    
                    return redirect('qr_check_in')
                else:
                    messages.error(request, 'Invalid QR code format!')
            except (IndexError, ValueError, User.DoesNotExist):
                messages.error(request, 'Invalid QR code!')
    else:
        form = QRCheckInForm()
    
    context = {
        'form': form,
        'gym': gym,
        'title': 'QR Code Check-In'
    }
    
    return render(request, 'analytics/qr_check_in.html', context)

@login_required
def check_out(request, attendance_id):
    """Check out a member"""
    if request.user.role != 'STAFF':
        messages.error(request, 'Only staff can check out members.')
        return redirect('home')
    
    staff_assignment = GymStaff.objects.filter(user=request.user).first()
    
    if not staff_assignment or not staff_assignment.can_check_in_members:
        messages.error(request, 'You do not have permission to check out members.')
        return redirect('staff_dashboard')
    
    attendance = get_object_or_404(Attendance, pk=attendance_id, gym=staff_assignment.gym)
    
    if attendance.check_out_time:
        messages.warning(request, f'{attendance.member.username} already checked out!')
    else:
        attendance.check_out_time = timezone.now()
        attendance.save()
        messages.success(request, f'{attendance.member.username} checked out successfully!')
    
    return redirect('check_in_dashboard')


# Analytics Dashboard Views

@login_required
def revenue_dashboard(request):
    """Revenue analytics for gym owners and staff with reports permission"""
    # Check if user is gym owner or staff with reports permission
    is_owner = request.user.role == 'GYM_OWNER'
    staff_assignment = None
    
    if request.user.role == 'STAFF':
        staff_assignment = GymStaff.objects.filter(user=request.user).first()
        if not staff_assignment or not staff_assignment.can_view_reports:
            messages.error(request, 'You do not have permission to view analytics.')
            return redirect('staff_dashboard')
    
    # Get gym
    if is_owner:
        gym = Gym.objects.filter(owner=request.user).first()
    else:
        gym = staff_assignment.gym
    
    if not gym:
        messages.error(request, 'No gym found.')
        return redirect('home')
    
    # Date range (last 30 days)
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    # Get payments for the gym
    payments = Payment.objects.filter(
        gym=gym,
        status='COMPLETED',
        created_at__date__gte=start_date
    )
    
    # Total revenue
    total_revenue = payments.aggregate(total=Sum('amount'))['total'] or 0
    
    # Revenue by payment method
    revenue_by_method = payments.values('payment_method').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    # Daily revenue for chart
    daily_revenue = payments.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    # Prepare chart data
    chart_labels = [item['date'].strftime('%b %d') for item in daily_revenue]
    chart_data = [float(item['total']) for item in daily_revenue]
    
    # Payment method chart data
    method_labels = [dict(Payment.PAYMENT_METHOD).get(item['payment_method'], item['payment_method']) for item in revenue_by_method]
    method_data = [float(item['total']) for item in revenue_by_method]
    
    context = {
        'title': 'Revenue Dashboard',
        'gym': gym,
        'total_revenue': total_revenue,
        'total_transactions': payments.count(),
        'revenue_by_method': revenue_by_method,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'method_labels': json.dumps(method_labels),
        'method_data': json.dumps(method_data),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'analytics/revenue_dashboard.html', context)

@login_required
def attendance_dashboard(request):
    """Attendance analytics dashboard"""
    # Check permissions
    is_owner = request.user.role == 'GYM_OWNER'
    staff_assignment = None
    
    if request.user.role == 'STAFF':
        staff_assignment = GymStaff.objects.filter(user=request.user).first()
        if not staff_assignment or not staff_assignment.can_view_reports:
            messages.error(request, 'You do not have permission to view analytics.')
            return redirect('staff_dashboard')
    
    # Get gym
    if is_owner:
        gym = Gym.objects.filter(owner=request.user).first()
    else:
        gym = staff_assignment.gym
    
    if not gym:
        messages.error(request, 'No gym found.')
        return redirect('home')
    
    # Date range (last 30 days)
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    # Get attendance records
    attendance_records = Attendance.objects.filter(
        gym=gym,
        check_in_time__date__gte=start_date
    )
    
    # Total check-ins
    total_checkins = attendance_records.count()
    
    # Average daily check-ins
    daily_checkins = attendance_records.annotate(
        date=TruncDate('check_in_time')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    avg_daily_checkins = attendance_records.annotate(
        date=TruncDate('check_in_time')
    ).values('date').annotate(
        count=Count('id')
    ).aggregate(avg=Avg('count'))['avg'] or 0
    
    # Today's check-ins
    today_checkins = attendance_records.filter(check_in_time__date=date.today()).count()
    
    # Prepare chart data
    chart_labels = [item['date'].strftime('%b %d') for item in daily_checkins]
    chart_data = [item['count'] for item in daily_checkins]
    
    # Peak hours analysis (hour of day)
    from django.db.models.functions import ExtractHour
    peak_hours = attendance_records.annotate(
        hour=ExtractHour('check_in_time')
    ).values('hour').annotate(
        count=Count('id')
    ).order_by('hour')
    
    hour_labels = [f"{item['hour']}:00" for item in peak_hours]
    hour_data = [item['count'] for item in peak_hours]
    
    context = {
        'title': 'Attendance Dashboard',
        'gym': gym,
        'total_checkins': total_checkins,
        'avg_daily_checkins': round(avg_daily_checkins, 1),
        'today_checkins': today_checkins,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'hour_labels': json.dumps(hour_labels),
        'hour_data': json.dumps(hour_data),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'analytics/attendance_dashboard.html', context)

@login_required
def member_dashboard(request):
    """Member analytics dashboard"""
    # Check permissions
    is_owner = request.user.role == 'GYM_OWNER'
    staff_assignment = None
    
    if request.user.role == 'STAFF':
        staff_assignment = GymStaff.objects.filter(user=request.user).first()
        if not staff_assignment or not staff_assignment.can_view_reports:
            messages.error(request, 'You do not have permission to view analytics.')
            return redirect('staff_dashboard')
    
    # Get gym
    if is_owner:
        gym = Gym.objects.filter(owner=request.user).first()
    elif request.user.role == 'STAFF' and staff_assignment:
        gym = staff_assignment.gym
    else:
        messages.error(request, 'You do not have permission to view analytics.')
        return redirect('home')
    
    if not gym:
        messages.error(request, 'No gym found.')
        return redirect('home')
    
    # Get memberships
    memberships = Membership.objects.filter(gym=gym)
    
    # Total members
    total_members = memberships.count()
    active_members = memberships.filter(is_active=True).count()
    inactive_members = memberships.filter(is_active=False).count()
    
    # Members by plan
    members_by_plan = memberships.filter(is_active=True).values('membership_plan__name').annotate(
        count=Count('id')
    )
    
    # New members over time (last 6 months)
    end_date = date.today()
    start_date = end_date - timedelta(days=180)
    
    monthly_signups = memberships.filter(
        joined_at__gte=start_date
    ).annotate(
        month=TruncMonth('joined_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Prepare chart data
    signup_labels = [item['month'].strftime('%b %Y') for item in monthly_signups]
    signup_data = [item['count'] for item in monthly_signups]
    
    plan_labels = [item['membership_plan__name'] or 'No Plan' for item in members_by_plan]
    plan_data = [item['count'] for item in members_by_plan]
    
    context = {
        'title': 'Member Dashboard',
        'gym': gym,
        'total_members': total_members,
        'active_members': active_members,
        'inactive_members': inactive_members,
        'members_by_plan': members_by_plan,
        'signup_labels': json.dumps(signup_labels),
        'signup_data': json.dumps(signup_data),
        'plan_labels': json.dumps(plan_labels),
        'plan_data': json.dumps(plan_data),
    }
    
    return render(request, 'analytics/member_dashboard.html', context)

