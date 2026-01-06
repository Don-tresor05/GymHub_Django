from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q
from .models import Payment
from .forms import PaymentForm
from gyms.models import GymStaff

@login_required
def process_payment(request):
    """Staff view to process a new payment"""
    try:
        staff = GymStaff.objects.get(user=request.user)
    except GymStaff.DoesNotExist:
        messages.error(request, "Only staff members can process payments.")
        return redirect('home')
    
    if not staff.can_process_payments:
        messages.error(request, "You don't have permission to process payments.")
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, gym=staff.gym)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.gym = staff.gym
            payment.processed_by = request.user
            payment.status = 'COMPLETED'  # Mark as completed immediately for cash/mobile money
            payment.save()
            
            messages.success(request, f"Payment processed successfully! Receipt: {payment.receipt_number}")
            return redirect('payment_receipt', payment.pk)
    else:
        form = PaymentForm(gym=staff.gym)
    
    return render(request, 'payments/process_payment.html', {
        'title': 'Process Payment',
        'form': form,
    })

@login_required
def payment_receipt(request, payment_id):
    """Display payment receipt"""
    payment = get_object_or_404(Payment, pk=payment_id)
    
    # Check permission
    try:
        staff = GymStaff.objects.get(user=request.user)
        if payment.gym != staff.gym:
            messages.error(request, "Permission denied.")
            return redirect('home')
    except GymStaff.DoesNotExist:
        # Allow user to view their own payments
        if payment.user != request.user:
            messages.error(request, "Permission denied.")
            return redirect('home')
    
    return render(request, 'payments/receipt.html', {
        'title': 'Payment Receipt',
        'payment': payment,
    })

@login_required
def payment_history(request):
    """Staff view to see payment history"""
    try:
        staff = GymStaff.objects.get(user=request.user)
    except GymStaff.DoesNotExist:
        messages.error(request, "Only staff members can view payment history.")
        return redirect('home')
    
    if not staff.can_view_reports:
        messages.error(request, "You don't have permission to view payment reports.")
        return redirect('staff_dashboard')
    
    # Get filter parameters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    payment_method = request.GET.get('payment_method')
    
    # Build query
    payments = Payment.objects.filter(gym=staff.gym).select_related('user', 'processed_by', 'membership')
    
    if date_from:
        payments = payments.filter(created_at__date__gte=date_from)
    if date_to:
        payments = payments.filter(created_at__date__lte=date_to)
    if payment_method:
        payments = payments.filter(payment_method=payment_method)
    
    # Calculate stats
    stats = payments.aggregate(
        total_revenue=Sum('amount'),
        total_count=Count('id')
    )
    
    # Payment method breakdown
    method_breakdown = payments.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('amount')
    )
    
    return render(request, 'payments/payment_history.html', {
        'title': 'Payment History',
        'payments': payments.order_by('-created_at'),
        'stats': stats,
        'method_breakdown': method_breakdown,
        'payment_methods': Payment.PAYMENT_METHOD,
    })

@login_required
def my_payments(request):
    """User view to see their own payment history"""
    payments = Payment.objects.filter(user=request.user).select_related('gym', 'membership').order_by('-created_at')
    
    total_paid = payments.filter(status='COMPLETED').aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, 'payments/my_payments.html', {
        'title': 'My Payments',
        'payments': payments,
        'total_paid': total_paid,
    })
