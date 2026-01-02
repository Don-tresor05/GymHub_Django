from django.urls import path
from .views import gym_list, gym_detail, gym_owner_dashboard, gym_detail_owner, gym_edit

urlpatterns = [
    path('', gym_list, name='gym_list'),
    path('dashboard/', gym_owner_dashboard, name='gym_owner_dashboard'),
    path('<int:pk>/', gym_detail, name='gym_detail'),
    path('manage/<int:pk>/', gym_detail_owner, name='gym_detail_owner'),
    path('manage/<int:pk>/edit/', gym_edit, name='gym_edit'),
]
