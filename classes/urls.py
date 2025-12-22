from django.urls import path
from .views import class_list

urlpatterns = [
    path('', class_list, name='class_list'),
]
