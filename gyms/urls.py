from django.urls import path
from .views import (gym_list, gym_detail, gym_owner_dashboard, gym_detail_owner, gym_edit,
                    gym_staff_management, update_staff_permissions, remove_staff,
                    manage_membership_plans, edit_membership_plan, delete_membership_plan,
                    manage_facilities, add_facility, edit_facility, delete_facility,
                    manage_equipment, add_equipment, edit_equipment, delete_equipment)

urlpatterns = [
    path('', gym_list, name='gym_list'),
    path('dashboard/', gym_owner_dashboard, name='gym_owner_dashboard'),
    path('<int:pk>/', gym_detail, name='gym_detail'),
    path('manage/<int:pk>/', gym_detail_owner, name='gym_detail_owner'),
    path('manage/<int:pk>/edit/', gym_edit, name='gym_edit'),
    path('manage/<int:pk>/staff/', gym_staff_management, name='gym_staff_management'),
    path('manage/<int:pk>/staff/<int:staff_id>/update/', update_staff_permissions, name='update_staff_permissions'),
    path('manage/<int:pk>/staff/<int:staff_id>/remove/', remove_staff, name='remove_staff'),
    path('manage/<int:pk>/membership-plans/', manage_membership_plans, name='manage_membership_plans'),
    path('manage/<int:pk>/membership-plans/<int:plan_id>/edit/', edit_membership_plan, name='edit_membership_plan'),
    path('manage/<int:pk>/membership-plans/<int:plan_id>/delete/', delete_membership_plan, name='delete_membership_plan'),
    
    # Facilities Management
    path('manage/<int:pk>/facilities/', manage_facilities, name='manage_facilities'),
    path('manage/<int:pk>/facilities/add/', add_facility, name='add_facility'),
    path('manage/<int:pk>/facilities/<int:facility_id>/edit/', edit_facility, name='edit_facility'),
    path('manage/<int:pk>/facilities/<int:facility_id>/delete/', delete_facility, name='delete_facility'),
    
    # Equipment Management
    path('manage/<int:pk>/equipment/', manage_equipment, name='manage_equipment'),
    path('manage/<int:pk>/equipment/add/', add_equipment, name='add_equipment'),
    path('manage/<int:pk>/equipment/<int:equipment_id>/edit/', edit_equipment, name='edit_equipment'),
    path('manage/<int:pk>/equipment/<int:equipment_id>/delete/', delete_equipment, name='delete_equipment'),
]
