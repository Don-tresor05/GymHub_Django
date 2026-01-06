from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_approved_display', 'is_active', 'date_joined')
    list_filter = ('role', 'is_approved', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'gym_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Approval', {
            'fields': ('role', 'is_approved', 'approval_date', 'approved_by', 'rejection_reason')
        }),
        ('Gym Owner Info', {
            'fields': ('gym_name', 'registration_document', 'pending_gym'),
            'classes': ('collapse',)
        }),
        ('Additional Info', {
            'fields': ('phone_number', 'date_of_birth', 'address', 'profile_photo', 'emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'email')}),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'approved_by', 'approval_date')
    
    actions = ['approve_gym_owners', 'reject_gym_owners']
    
    def is_approved_display(self, obj):
        if obj.role == 'MEMBER':
            return format_html('<span style="color: green;">✓ Auto</span>')
        elif obj.is_approved:
            return format_html('<span style="color: green;">✓ Approved</span>')
        else:
            return format_html('<span style="color: orange;">⏳ Pending</span>')
    is_approved_display.short_description = 'Approval Status'
    
    def approve_gym_owners(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(role='GYM_OWNER', is_approved=False).update(
            is_approved=True,
            is_active=True,
            approved_by=request.user,
            approval_date=timezone.now()
        )
        self.message_user(request, f'{updated} gym owner(s) approved successfully.')
    approve_gym_owners.short_description = 'Approve selected gym owners'
    
    def reject_gym_owners(self, request, queryset):
        updated = queryset.filter(role='GYM_OWNER', is_approved=False).update(
            rejection_reason='Rejected by admin'
        )
        self.message_user(request, f'{updated} gym owner(s) rejected.')
    reject_gym_owners.short_description = 'Reject selected gym owners'

