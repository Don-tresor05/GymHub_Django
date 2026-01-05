from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from .models import User
from .forms import CustomUserCreationForm, GymOwnerRegistrationForm, UserUpdateForm, UnifiedRegistrationForm

class CustomLoginView(LoginView):
    """Custom login view with role-based redirects"""
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        user = self.request.user
        
        if user.role == 'GYM_OWNER':
            return '/gyms/dashboard/'
        elif user.role == 'STAFF':
            return '/accounts/staff/dashboard/'
        elif user.role == 'MEMBER':
            return '/accounts/dashboard/'
        elif user.role == 'TRAINER':
            return '/trainers/dashboard/'
        else:
            return '/'

def home_view(request):
    """Home page view - redirect authenticated users to their dashboard"""
    if request.user.is_authenticated:
        # Redirect to appropriate dashboard based on role
        user_role = getattr(request.user, 'role', None)
        
        if user_role == 'GYM_OWNER':
            return redirect('gym_owner_dashboard')
        elif user_role == 'STAFF':
            return redirect('staff_dashboard')
        elif user_role in ['MEMBER', 'TRAINER']:
            return redirect('member_dashboard')
    
    # Show home page only for unauthenticated users
    from gyms.models import Gym
    gyms = Gym.objects.all()[:6]  # Show first 6 gyms on home page
    return render(request, 'home.html', {'gyms': gyms})

def register_view(request):
    """Unified registration view for all roles"""
    if request.method == 'POST':
        form = UnifiedRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            role = user.role
            
            if role == 'MEMBER':
                # Auto-login for members
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, f'Registration successful! Welcome to {form.cleaned_data.get("gym").name}!')
                return redirect('member_dashboard')
            elif role == 'GYM_OWNER':
                messages.success(request, 'Registration submitted! Your account is pending admin approval. You will be notified via email once approved.')
                return redirect('login')
            elif role in ['STAFF', 'TRAINER']:
                messages.success(request, f'Registration submitted! Your {role.lower()} request is pending approval from {form.cleaned_data.get("pending_gym").name}.')
                return redirect('login')
    else:
        # Exclude GYM_OWNER from regular registration
        form = UnifiedRegistrationForm(exclude_roles=['GYM_OWNER'])
    
    context = {
        'form': form, 
        'title': 'Join as Member, Staff or Trainer'
    }
    return render(request, 'accounts/unified_register.html', context)

def gym_owner_register_view(request):
    """Specialized Gym Owner registration view"""
    if request.method == 'POST':
        form = UnifiedRegistrationForm(request.POST, request.FILES, exclude_roles=['MEMBER', 'STAFF', 'TRAINER', 'ADMIN'])
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Gym owner registration submitted! Your account is pending admin approval. You will be notified via email once approved.')
            return redirect('login')
    else:
        # Only allow GYM_OWNER role
        form = UnifiedRegistrationForm(exclude_roles=['MEMBER', 'STAFF', 'TRAINER', 'ADMIN'])
        # Set GYM_OWNER as the only and default option
        form.fields['role'].initial = 'GYM_OWNER'
    
    return render(request, 'accounts/unified_register.html', {'form': form, 'title': 'Register Your Gym', 'is_gym_owner': True})

@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def member_dashboard(request):
    """Dashboard for regular members"""
    if request.user.role != 'MEMBER':
        # Redirect based on role
        if request.user.role == 'GYM_OWNER':
            return redirect('gym_owner_dashboard')
        elif request.user.role == 'STAFF':
            return redirect('staff_dashboard')
        elif request.user.role == 'TRAINER':
            return redirect('trainer_dashboard')
        else:
            return redirect('home')
    
    from members.models import Membership
    from classes.models import GymClass
    from payments.models import Payment
    from django.utils import timezone
    
    # Get user's membership
    membership = Membership.objects.filter(user=request.user, is_active=True).first()
    
    if not membership:
        messages.warning(request, 'You are not a member of any gym yet.')
        return redirect('gym_list')
    
    # Get gym details
    gym = membership.gym
    
    # Get available classes at user's gym
    upcoming_classes = GymClass.objects.filter(
        gym=gym, 
        start_time__gte=timezone.now()
    ).order_by('start_time')[:5]
    
    # Get recent payments
    recent_payments = Payment.objects.filter(
        user=request.user,
        gym=gym
    ).order_by('-created_at')[:5]
    
    context = {
        'membership': membership,
        'gym': gym,
        'upcoming_classes': upcoming_classes,
        'recent_payments': recent_payments,
        'title': 'My Dashboard'
    }
    
    return render(request, 'accounts/member_dashboard.html', context)

@login_required
def staff_dashboard(request):
    """Dashboard for gym staff"""
    from gyms.models import GymStaff
    from members.models import Membership
    from payments.models import Payment
    from django.utils import timezone
    from datetime import date
    
    if request.user.role != 'STAFF':
        return redirect('member_dashboard')
    
    # Get staff assignment
    staff_assignment = GymStaff.objects.filter(user=request.user).first()
    
    if not staff_assignment:
        messages.error(request, 'You are not assigned to any gym as staff.')
        return redirect('home')
    
    gym = staff_assignment.gym
    
    # Today's stats
    today_members = Membership.objects.filter(
        gym=gym,
        is_active=True,
        joined_at__date=date.today()
    ).count()
    
    total_active_members = Membership.objects.filter(gym=gym, is_active=True).count()
    
    # Today's payments
    today_revenue = Payment.objects.filter(
        gym=gym,
        created_at__date=date.today(),
        status='COMPLETED'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent payments
    recent_payments = Payment.objects.filter(gym=gym).order_by('-created_at')[:10]
    
    context = {
        'staff_assignment': staff_assignment,
        'gym': gym,
        'today_members': today_members,
        'total_active_members': total_active_members,
        'today_revenue': today_revenue,
        'recent_payments': recent_payments,
        'title': 'Staff Dashboard'
    }
    
    return render(request, 'accounts/staff_dashboard.html', context)

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

# ========== APPROVAL VIEWS ==========

@login_required
def pending_staff_approvals(request):
    """Gym owner view to approve/reject staff and trainer requests"""
    from gyms.models import Gym
    from django.utils import timezone
    
    if request.user.role != 'GYM_OWNER':
        messages.error(request, 'Only gym owners can access this page.')
        return redirect('home')
    
    # Get gyms owned by this user
    my_gyms = Gym.objects.filter(owner=request.user)
    
    # Get pending staff/trainers for my gyms
    pending_users = User.objects.filter(
        pending_gym__in=my_gyms,
        is_approved=False,
        role__in=['STAFF', 'TRAINER']
    ).select_related('pending_gym')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        rejection_reason = request.POST.get('rejection_reason', '')
        
        user = get_object_or_404(User, pk=user_id, pending_gym__in=my_gyms, is_approved=False)
        
        if action == 'approve':
            from gyms.models import GymStaff
            
            user.is_approved = True
            user.is_active = True
            user.approved_by = request.user
            user.approval_date = timezone.now()
            user.save()
            
            # Create GymStaff assignment
            GymStaff.objects.create(
                user=user,
                gym=user.pending_gym,
                role=user.role,
                assigned_by=request.user,
                can_check_in_members=True if user.role == 'STAFF' else False,
                can_process_payments=True if user.role == 'STAFF' else False,
                can_manage_classes=True if user.role == 'TRAINER' else False,
            )
            
            messages.success(request, f'{user.username} has been approved as {user.get_role_display()} at {user.pending_gym.name}!')
        elif action == 'reject':
            user.rejection_reason = rejection_reason
            user.save()
            messages.warning(request, f'{user.username} has been rejected.')
    
    context = {
        'pending_users': pending_users,
        'title': 'Pending Staff & Trainer Approvals'
    }
    return render(request, 'accounts/gym_owner_approvals.html', context)

@login_required
def promote_member(request, member_id):
    """Gym owner can promote a member to staff or trainer"""
    from gyms.models import Gym, GymStaff
    from members.models import Membership
    from django.utils import timezone
    
    if request.user.role != 'GYM_OWNER':
        messages.error(request, 'Only gym owners can promote members.')
        return redirect('home')
    
    member = get_object_or_404(User, pk=member_id, role='MEMBER')
    
    # Get gym owner's gyms
    my_gyms = Gym.objects.filter(owner=request.user)
    
    # Check if member belongs to one of the owner's gyms
    membership = Membership.objects.filter(user=member, gym__in=my_gyms, is_active=True).first()
    
    if not membership:
        messages.error(request, 'This member does not belong to any of your gyms.')
        return redirect('gym_owner_dashboard')
    
    if request.method == 'POST':
        new_role = request.POST.get('new_role')
        
        if new_role not in ['STAFF', 'TRAINER']:
            messages.error(request, 'Invalid role selection.')
            return redirect('gym_owner_dashboard')
        
        # Update user role
        member.role = new_role
        member.save()
        
        # Create GymStaff assignment
        GymStaff.objects.create(
            user=member,
            gym=membership.gym,
            role=new_role,
            assigned_by=request.user,
            can_check_in_members=True if new_role == 'STAFF' else False,
            can_process_payments=True if new_role == 'STAFF' else False,
            can_manage_classes=True if new_role == 'TRAINER' else False,
        )
        
        messages.success(request, f'{member.username} has been promoted to {new_role} at {membership.gym.name}!')
        return redirect('gym_owner_dashboard')
    
    context = {
        'member': member,
        'membership': membership,
        'title': f'Promote {member.username}'
    }
    return render(request, 'accounts/promote_member.html', context)