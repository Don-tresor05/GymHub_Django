from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Membership

@login_required
def upgrade_membership(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, user=request.user)
    from members.models import MembershipPlan
    plans = MembershipPlan.objects.filter(gym=membership.gym, is_active=True).order_by('price')
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        try:
            plan = MembershipPlan.objects.get(id=plan_id, gym=membership.gym, is_active=True)
        except MembershipPlan.DoesNotExist:
            messages.error(request, 'Invalid plan selected.')
            return redirect('member_dashboard')
        membership.membership_plan = plan
        from django.utils import timezone
        membership.expires_at = timezone.now() + timezone.timedelta(days=plan.duration_days)
        membership.save()
        messages.success(request, 'Membership upgraded successfully!')
        return redirect('member_dashboard')
    return render(request, 'accounts/upgrade_membership.html', {
        'membership': membership,
        'plans': plans,
    })