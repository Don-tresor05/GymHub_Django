from django.contrib import admin
from .models import Membership, MembershipPlan

@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'tier', 'duration', 'price', 'duration_days', 'is_active')
    list_filter = ('tier', 'duration', 'is_active', 'gym')
    search_fields = ('name', 'gym__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym', 'membership_plan', 'status', 'joined_at', 'expires_at', 'is_active')
    list_filter = ('status', 'is_active', 'is_family_plan', 'gym')
    search_fields = ('user__username', 'user__email', 'gym__name', 'qr_code')
    readonly_fields = ('qr_code', 'joined_at')
    date_hierarchy = 'joined_at'
