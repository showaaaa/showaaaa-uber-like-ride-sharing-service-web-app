# from django.db.models.signals import post_save
# from .models import Vehicle
# from django.dispatch import receiver
# from django.contrib.auth.models import User

# @receiver(post_save, sender=User)
# def create_driver_info(sender, instance, created, **kwargs):
#     if created:
#         Vehicle.objects.create(owner=instance)


# @receiver(post_save, sender=User)
# def save_driver_info(sender, instance, **kwargs):
#     instance.vehicle.save()

