from django.urls import path
from .views import trainer_dashboard, manage_availability, manage_clients, performance_analytics, earnings_summary

urlpatterns = [
    path('dashboard/', trainer_dashboard, name='trainer_dashboard'),
    path('availability/', manage_availability, name='trainer_availability'),
    path('clients/', manage_clients, name='trainer_clients'),
    path('performance/', performance_analytics, name='trainer_performance'),
    path('earnings/', earnings_summary, name='trainer_earnings'),
]
