# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
from allauth.socialaccount.signals import social_account_added, social_account_updated

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # get_or_create ensures old users without a profile get one automatically
        profile, created_profile = UserProfile.objects.get_or_create(user=instance)
        if not created_profile:
            profile.save()


@receiver([social_account_added, social_account_updated])
def populate_google_profile(request, sociallogin, **kwargs):
    if sociallogin.account.provider == 'google':
        picture_url = sociallogin.account.extra_data.get('picture')
        user = sociallogin.account.user
        
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if picture_url:
            profile.avatar_url = picture_url
            profile.save()