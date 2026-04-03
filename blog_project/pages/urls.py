"""Pages app URL configuration."""

from django.urls import path
from pages import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter'),
]
