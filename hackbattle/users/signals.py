# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Profile,Hospital


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         obj=Profile.objects.create(user=instance)
#         if obj.is_hospital==True:
#             Hospital.objects.create(user=instance)



# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     if instance.profile.is_hospital:
#         instance.hospital.save()
