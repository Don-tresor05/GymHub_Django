from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    path('receipt/<int:payment_id>/', views.payment_receipt, name='payment_receipt'),
    path('history/', views.payment_history, name='payment_history'),
    path('my-payments/', views.my_payments, name='my_payments'),
]
