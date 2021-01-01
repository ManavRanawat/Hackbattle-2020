from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Hospital


@receiver(post_save, sender=Profile)
def create_hospital(sender, instance, created, **kwargs):
    print("HIIIIIIIIIIIIIIIIII")
    print(instance)
    print(created)
    if created:
        if instance.is_hospital==True:
            Hospital.objects.create(user=instance.user)

@receiver(post_save, sender=Profile)
def save_hospital(sender, instance, **kwargs):
    print(instance,end="   ")
    print("  SAVED")
    if instance.is_hospital:
        instance.user.hospital.save()
