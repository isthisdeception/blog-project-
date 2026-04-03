"""
Accounts models - Extended user profile with custom fields.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Profile(models.Model):
    """
    Extended user profile with additional fields beyond Django's default User model.
    Created automatically via signal when a new user is registered.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile customization
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself...")
    profile_picture = models.ImageField(
        upload_to='profile_pics/%Y/%m/%d/', 
        null=True,
        blank=True,
    )
    website = models.URLField(blank=True, max_length=200)
    location = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return f'{self.user.username}\'s Profile'


# Automatically create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Auto-save the Profile whenever the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
