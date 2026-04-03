"""Accounts admin - Profile management in Django admin."""

from django.contrib import admin
from accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'created_at']
    search_fields = ['user__username', 'location']
    list_filter = ['created_at']
