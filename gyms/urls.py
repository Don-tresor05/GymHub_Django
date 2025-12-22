from django.urls import path
from .views import gym_list

urlpatterns = [
    path('', gym_list, name='gym_list'),
]
