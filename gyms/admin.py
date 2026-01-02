from django.contrib import admin
from .models import Gym

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'contact_phone', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('name', 'address', 'contact_phone', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
