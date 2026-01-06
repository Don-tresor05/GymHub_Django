from django.urls import path
from .views import upgrade_membership

urlpatterns = [
    path('upgrade/<int:membership_id>/', upgrade_membership, name='upgrade_membership'),
]
