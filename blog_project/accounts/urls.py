"""Accounts app URL configuration."""

from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile/change-password/', views.change_password, name='change-password'),
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
]
