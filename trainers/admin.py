from django.contrib import admin
from .models import TrainerProfile, TrainerAvailability, ClientAssignment, TrainerCommission

@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'years_experience', 'hourly_rate', 'is_freelance')
    list_filter = ('is_freelance',)
    search_fields = ('user__username', 'specialties')

@admin.register(TrainerAvailability)
class TrainerAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('trainer__user__username',)

@admin.register(ClientAssignment)
class ClientAssignmentAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'member', 'gym', 'assigned_at', 'is_active')
    list_filter = ('is_active', 'gym', 'assigned_at')
    search_fields = ('trainer__user__username', 'member__username')
    date_hierarchy = 'assigned_at'

@admin.register(TrainerCommission)
class TrainerCommissionAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'session_date', 'amount', 'is_paid', 'paid_date')
    list_filter = ('is_paid', 'session_date', 'paid_date')
    search_fields = ('trainer__user__username', 'description')
    date_hierarchy = 'session_date'
