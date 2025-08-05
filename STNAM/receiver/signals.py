# receiver/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ReceiverProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_receiver_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'receiver':  # make sure User model has `role`
        ReceiverProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_receiver_profile(sender, instance, **kwargs):
    if instance.role == 'receiver':
        instance.receiverprofile.save()
