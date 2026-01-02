from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view, gym_owner_register_view, edit_profile_view, join_gym_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('gym-owner/register/', gym_owner_register_view, name='gym_owner_register'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('join-gym/<int:gym_id>/', join_gym_view, name='join_gym'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
