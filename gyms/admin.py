from django.contrib import admin
from .models import Gym, GymFacility, Equipment, GymStaff

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'contact_phone', 'opening_time', 'closing_time', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'address', 'contact_phone', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'owner', 'description', 'image')
        }),
        ('Contact & Location', {
            'fields': ('address', 'contact_phone')
        }),
        ('Operating Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Pricing', {
            'fields': ('basic_price', 'premium_price', 'corporate_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GymFacility)
class GymFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'facility_type', 'is_available')
    list_filter = ('facility_type', 'is_available', 'gym')
    search_fields = ('name', 'gym__name')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'gym', 'status', 'last_maintenance', 'next_maintenance')
    list_filter = ('status', 'gym')
    search_fields = ('name', 'brand', 'gym__name')

@admin.register(GymStaff)
class GymStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym', 'role', 'is_active', 'assigned_at')
    list_filter = ('role', 'is_active', 'gym')
    search_fields = ('user__username', 'user__email', 'gym__name')
    readonly_fields = ('assigned_at', 'assigned_by')
    fieldsets = (
        ('Assignment', {
            'fields': ('gym', 'user', 'role', 'assigned_by', 'assigned_at', 'is_active')
        }),
        ('Permissions', {
            'fields': ('can_check_in_members', 'can_process_payments', 'can_manage_classes', 'can_view_reports')
        }),
    )
