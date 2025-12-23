from django.urls import path
from .views import gym_list, gym_detail, gym_owner_dashboard

urlpatterns = [
    path('', gym_list, name='gym_list'),
    path('dashboard/', gym_owner_dashboard, name='gym_owner_dashboard'),
    path('<int:pk>/', gym_detail, name='gym_detail'),
]
