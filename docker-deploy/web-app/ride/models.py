from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

TYPE_CHOICES = (
    ("SUV", "SUV"),
    ("COMPACT", "COMPACT"),
    ("F1", "F1"),
    ("--", "--"),
)
# Create your models here.
class Ride(models.Model):
    rideOwner          = models.ForeignKey(User, related_name='rideOwner', on_delete=models.CASCADE)
    driver             = models.ForeignKey(User, related_name='driver', on_delete=models.CASCADE, null=True, blank=True)
    sharer             = models.ManyToManyField(get_user_model(), related_name='share', blank=True)
    # SharerOrders        = models.ManyToManyField(SharerOrder, related_name='driver', null=True, blank=True)
    destAddr           = models.CharField(max_length=50)
    date               = models.DateTimeField(help_text='Format: 2023-01-01 12:00')
    #time               = models.TimeField(auto_now=False)
    vehicleType        = models.CharField(max_length=20, choices=TYPE_CHOICES, default='--')
    numPeople          = models.PositiveIntegerField(default=1)
    allowSharernum        = models.PositiveIntegerField(help_text='No sharer please choose 0', default=0, blank=True)
    shared             = models.BooleanField(default=False)
    specRequest        = models.CharField(max_length=200, blank=True)
    maxPeople          =models.PositiveIntegerField(help_text='numPeople + allowSharernum', default=4)
    class STATUS(models.IntegerChoices):
        opened    = 1
        confirmed = 2
        completed = 3 
    status             = models.IntegerField(default=1, choices=STATUS.choices)

    def __str__(self):
        return self.destAddr

    def get_absolute_url(self):
        return reverse('ride-detail', kwargs={'pk': self.pk})

class SharerOrder(models.Model):
    orderOwner          = models.ForeignKey(User, related_name='orderOwner', on_delete=models.CASCADE)
    sharerride                = models.ForeignKey(Ride, related_name='sharerride', on_delete = models.CASCADE,null=True, blank=True)
    destAddr           = models.CharField(max_length=50)
    numPeople          = models.IntegerField(default=1)
    earliestDate               = models.DateTimeField(help_text='Format: 2023-01-01 12:00')
    latestDate             = models.DateTimeField(help_text='Format: 2023-01-01 12:00')

    def __str__(self):
        return self.destAddr

    # after submit, fo this url
    def get_absolute_url(self):
        return reverse('sharerorder-list')