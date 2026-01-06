from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (register_view, profile_view, gym_owner_register_view, 
                    edit_profile_view, join_gym_view, member_dashboard, staff_dashboard, CustomLoginView,
                    pending_staff_approvals, promote_member)
from .api import get_membership_plans

urlpatterns = [
    path('register/', register_view, name='register'),
    path('gym-owner/register/', gym_owner_register_view, name='gym_owner_register'),
    path('dashboard/', member_dashboard, name='member_dashboard'),
    path('staff/dashboard/', staff_dashboard, name='staff_dashboard'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('join-gym/<int:gym_id>/', join_gym_view, name='join_gym'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('staff-approvals/', pending_staff_approvals, name='staff_approvals'),
    path('promote-member/<int:member_id>/', promote_member, name='promote_member'),
    # API endpoints
    path('api/membership-plans/<int:gym_id>/', get_membership_plans, name='get_membership_plans'),
]
