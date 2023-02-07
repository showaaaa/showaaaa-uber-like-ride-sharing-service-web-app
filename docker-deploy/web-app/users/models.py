from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ("SUV", "SUV"),
    ("COMPACT", "COMPACT"),
    ("F1", "F1"),
    ("--", "--"),
)

class Vehicle(models.Model):   
    owner = models.OneToOneField(User, on_delete = models.CASCADE)
    license_number = models.CharField(max_length = 10)
    capacity = models.PositiveIntegerField(default = 4)
    vehicle_type = models.CharField(max_length = 20, choices = TYPE_CHOICES, default = 'COMPACT')
    special_info = models.TextField(max_length = 200, blank = True)

    def __str__(self):
        return f'{self.owner.username} Vehicle'