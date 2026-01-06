from django.contrib import admin
from .models import Attendance, GuestPass

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('member', 'gym', 'gym_class', 'check_in_time', 'check_out_time', 'is_qr_checkin', 'get_duration')
    list_filter = ('gym', 'is_qr_checkin', 'check_in_time')
    search_fields = ('member__username', 'gym__name')
    date_hierarchy = 'check_in_time'
    readonly_fields = ('check_in_time',)

@admin.register(GuestPass)
class GuestPassAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'gym', 'guest_phone', 'status', 'issued_at', 'valid_until')
    list_filter = ('status', 'gym', 'issued_at')
    search_fields = ('guest_name', 'guest_phone', 'guest_email')
    date_hierarchy = 'issued_at'
    readonly_fields = ('issued_at',)
