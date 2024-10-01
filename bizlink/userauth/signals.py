from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    print(f"Signal triggered for user: {instance.username}")  # Debugging line
    if created:
        Profile.objects.create(created_by=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # Check if the profile exists before trying to save it
    if hasattr(instance, 'user_profile'):
        instance.user_profile.save()