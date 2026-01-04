from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.contrib import messages
from .models import Gym, GymStaff, GymFacility, Equipment
from .forms import GymUpdateForm, AssignStaffForm, UpdateStaffPermissionsForm, MembershipPlanForm
from .forms_facilities import GymFacilityForm, EquipmentForm
from members.models import Membership, MembershipPlan
from payments.models import Payment
from classes.models import GymClass
from accounts.models import User
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

@login_required
def gym_staff_management(request, pk):
    """Manage staff and trainers for a gym"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    
    staff_members = GymStaff.objects.filter(gym=gym).select_related('user')
    
    # Get users who are not gym owners and not already assigned to this gym
    assigned_user_ids = staff_members.values_list('user_id', flat=True)
    available_users = User.objects.exclude(
        id__in=assigned_user_ids
    ).exclude(
        role='GYM_OWNER'
    ).exclude(
        id=request.user.id
    ).order_by('username')
    
    if request.method == 'POST':
        form = AssignStaffForm(request.POST, gym=gym)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.gym = gym
            staff.assigned_by = request.user
            staff.save()
            messages.success(request, f'{staff.user.username} has been assigned as {staff.get_role_display()}!')
            return redirect('gym_staff_management', pk=gym.pk)
    else:
        form = AssignStaffForm(gym=gym)
    
    context = {
        'gym': gym,
        'staff_members': staff_members,
        'form': form,
        'available_users': available_users,
    }
    
    return render(request, 'gyms/staff_management.html', context)

@login_required
def update_staff_permissions(request, pk, staff_id):
    """Update staff member permissions"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    staff = get_object_or_404(GymStaff, pk=staff_id, gym=gym)
    
    if request.method == 'POST':
        form = UpdateStaffPermissionsForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, f'Permissions updated for {staff.user.username}!')
            return redirect('gym_staff_management', pk=gym.pk)
    else:
        form = UpdateStaffPermissionsForm(instance=staff)
    
    return render(request, 'gyms/update_staff_permissions.html', {'form': form, 'gym': gym, 'staff': staff})

@login_required
def remove_staff(request, pk, staff_id):
    """Remove staff member from gym"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    staff = get_object_or_404(GymStaff, pk=staff_id, gym=gym)
    
    if request.method == 'POST':
        username = staff.user.username
        staff.delete()
        messages.success(request, f'{username} has been removed from your staff.')
        return redirect('gym_staff_management', pk=gym.pk)
    
    return render(request, 'gyms/confirm_remove_staff.html', {'gym': gym, 'staff': staff})

@login_required
def manage_membership_plans(request, pk):
    """Manage membership plans for a gym"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    plans = MembershipPlan.objects.filter(gym=gym)
    
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.gym = gym
            plan.save()
            messages.success(request, f'Membership plan "{plan.name}" created successfully!')
            return redirect('manage_membership_plans', pk=gym.pk)
    else:
        form = MembershipPlanForm()
    
    context = {
        'gym': gym,
        'plans': plans,
        'form': form,
    }
    
    return render(request, 'gyms/membership_plans.html', context)

@login_required
def edit_membership_plan(request, pk, plan_id):
    """Edit a membership plan"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    plan = get_object_or_404(MembershipPlan, pk=plan_id, gym=gym)
    
    if request.method == 'POST':
        form = MembershipPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, f'Membership plan "{plan.name}" updated successfully!')
            return redirect('manage_membership_plans', pk=gym.pk)
    else:
        form = MembershipPlanForm(instance=plan)
    
    return render(request, 'gyms/edit_membership_plan.html', {'form': form, 'gym': gym, 'plan': plan})

@login_required
def delete_membership_plan(request, pk, plan_id):
    """Delete a membership plan"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    plan = get_object_or_404(MembershipPlan, pk=plan_id, gym=gym)
    
    if request.method == 'POST':
        plan_name = plan.name
        plan.delete()
        messages.success(request, f'Membership plan "{plan_name}" deleted successfully!')
        return redirect('manage_membership_plans', pk=gym.pk)
    
    return render(request, 'gyms/confirm_delete_plan.html', {'gym': gym, 'plan': plan})


# Facilities Management Views

@login_required
def manage_facilities(request, pk):
    """View for gym owner to manage facilities"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    facilities = GymFacility.objects.filter(gym=gym)
    
    return render(request, 'gyms/manage_facilities.html', {
        'title': 'Manage Facilities',
        'gym': gym,
        'facilities': facilities,
    })

@login_required
def add_facility(request, pk):
    """Add a new facility to the gym"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = GymFacilityForm(request.POST)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.gym = gym
            facility.save()
            messages.success(request, f'Facility "{facility.name}" added successfully!')
            return redirect('manage_facilities', pk=gym.pk)
    else:
        form = GymFacilityForm()
    
    return render(request, 'gyms/add_facility.html', {
        'title': 'Add Facility',
        'gym': gym,
        'form': form,
    })

@login_required
def edit_facility(request, pk, facility_id):
    """Edit an existing facility"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    facility = get_object_or_404(GymFacility, pk=facility_id, gym=gym)
    
    if request.method == 'POST':
        form = GymFacilityForm(request.POST, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, f'Facility "{facility.name}" updated successfully!')
            return redirect('manage_facilities', pk=gym.pk)
    else:
        form = GymFacilityForm(instance=facility)
    
    return render(request, 'gyms/edit_facility.html', {
        'title': 'Edit Facility',
        'gym': gym,
        'facility': facility,
        'form': form,
    })

@login_required
def delete_facility(request, pk, facility_id):
    """Delete a facility"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    facility = get_object_or_404(GymFacility, pk=facility_id, gym=gym)
    
    if request.method == 'POST':
        facility_name = facility.name
        facility.delete()
        messages.success(request, f'Facility "{facility_name}" deleted successfully!')
        return redirect('manage_facilities', pk=gym.pk)
    
    return render(request, 'gyms/confirm_delete_facility.html', {
        'gym': gym,
        'facility': facility,
    })


# Equipment Management Views

@login_required
def manage_equipment(request, pk):
    """View for gym owner to manage equipment"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    equipment = Equipment.objects.filter(gym=gym)
    
    # Calculate stats
    total_equipment = equipment.count()
    working_count = equipment.filter(status='WORKING').count()
    maintenance_count = equipment.filter(status='MAINTENANCE').count()
    broken_count = equipment.filter(status='BROKEN').count()
    
    return render(request, 'gyms/manage_equipment.html', {
        'title': 'Manage Equipment',
        'gym': gym,
        'equipment': equipment,
        'total_equipment': total_equipment,
        'working_count': working_count,
        'maintenance_count': maintenance_count,
        'broken_count': broken_count,
    })

@login_required
def add_equipment(request, pk):
    """Add new equipment to the gym"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            equipment = form.save(commit=False)
            equipment.gym = gym
            equipment.save()
            messages.success(request, f'Equipment "{equipment.name}" added successfully!')
            return redirect('manage_equipment', pk=gym.pk)
    else:
        form = EquipmentForm()
    
    return render(request, 'gyms/add_equipment.html', {
        'title': 'Add Equipment',
        'gym': gym,
        'form': form,
    })

@login_required
def edit_equipment(request, pk, equipment_id):
    """Edit existing equipment"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    equipment = get_object_or_404(Equipment, pk=equipment_id, gym=gym)
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Equipment "{equipment.name}" updated successfully!')
            return redirect('manage_equipment', pk=gym.pk)
    else:
        form = EquipmentForm(instance=equipment)
    
    return render(request, 'gyms/edit_equipment.html', {
        'title': 'Edit Equipment',
        'gym': gym,
        'equipment': equipment,
        'form': form,
    })

@login_required
def delete_equipment(request, pk, equipment_id):
    """Delete equipment"""
    gym = get_object_or_404(Gym, pk=pk, owner=request.user)
    equipment = get_object_or_404(Equipment, pk=equipment_id, gym=gym)
    
    if request.method == 'POST':
        equipment_name = equipment.name
        equipment.delete()
        messages.success(request, f'Equipment "{equipment_name}" deleted successfully!')
        return redirect('manage_equipment', pk=gym.pk)
    
    return render(request, 'gyms/confirm_delete_equipment.html', {
        'gym': gym,
        'equipment': equipment,
    })


