from django.http import JsonResponse
from members.models import MembershipPlan

def get_membership_plans(request, gym_id):
    """API endpoint to get membership plans for a gym"""
    plans = MembershipPlan.objects.filter(gym_id=gym_id, is_active=True).values(
        'id', 'name', 'tier', 'duration', 'price', 'duration_days', 'description'
    )
    return JsonResponse(list(plans), safe=False)
