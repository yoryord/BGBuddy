from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from BoardGameBuddy.account.models import BuddyProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_buddy_profile(instance, created, **kwargs):
    """
    Once a new 'BuddyAccount' instance is saved creates a BuddyProfile for it.
    """
    if not created:
        return

    instance.buddyprofile = BuddyProfile.objects.create(account_id=instance)
