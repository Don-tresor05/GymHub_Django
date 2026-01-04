from django.urls import path
from .views import (check_in_dashboard, manual_check_in, qr_check_in, check_out,
                    revenue_dashboard, attendance_dashboard, member_dashboard)

urlpatterns = [
    # Check-in system
    path('check-in/', check_in_dashboard, name='check_in_dashboard'),
    path('check-in/manual/', manual_check_in, name='manual_check_in'),
    path('check-in/qr/', qr_check_in, name='qr_check_in'),
    path('check-out/<int:attendance_id>/', check_out, name='check_out'),
    
    # Analytics dashboards
    path('revenue/', revenue_dashboard, name='revenue_dashboard'),
    path('attendance/', attendance_dashboard, name='attendance_dashboard'),
    path('members/', member_dashboard, name='member_dashboard'),
]
