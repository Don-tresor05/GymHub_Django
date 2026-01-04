from django.urls import path
from .views import class_list, class_detail, book_class, cancel_booking, my_bookings

urlpatterns = [
    path('', class_list, name='class_list'),
    path('<int:pk>/', class_detail, name='class_detail'),
    path('<int:pk>/book/', book_class, name='book_class'),
    path('booking/<int:pk>/cancel/', cancel_booking, name='cancel_booking'),
    path('my-bookings/', my_bookings, name='my_bookings'),
]
