from django.urls import path
from .views import gym_list, gym_detail

urlpatterns = [
    path('', gym_list, name='gym_list'),
    path('<int:pk>/', gym_detail, name='gym_detail'),
]
