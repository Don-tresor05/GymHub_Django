from django.contrib import admin
from .models import GymClass, ClassBooking, ClassWaitlist

@admin.register(GymClass)
class GymClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_type', 'gym', 'trainer', 'start_time', 'capacity', 'get_enrolled_count', 'is_cancelled')
    list_filter = ('class_type', 'gym', 'is_recurring', 'is_cancelled', 'start_time')
    search_fields = ('name', 'gym__name', 'trainer__username')
    date_hierarchy = 'start_time'
    
    def get_enrolled_count(self, obj):
        return obj.get_enrolled_count()
    get_enrolled_count.short_description = 'Enrolled'

@admin.register(ClassBooking)
class ClassBookingAdmin(admin.ModelAdmin):
    list_display = ('member', 'gym_class', 'status', 'booked_at')
    list_filter = ('status', 'booked_at')
    search_fields = ('member__username', 'gym_class__name')
    date_hierarchy = 'booked_at'

@admin.register(ClassWaitlist)
class ClassWaitlistAdmin(admin.ModelAdmin):
    list_display = ('member', 'gym_class', 'joined_at', 'is_notified')
    list_filter = ('is_notified', 'joined_at')
    search_fields = ('member__username', 'gym_class__name')
    date_hierarchy = 'joined_at'
