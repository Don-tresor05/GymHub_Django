from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'gym', 'amount', 'payment_method', 'payment_type', 'status', 'receipt_number', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_type', 'gym', 'created_at')
    search_fields = ('user__username', 'transaction_id', 'receipt_number', 'mobile_money_number')
    readonly_fields = ('transaction_id', 'receipt_number', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
