from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
import os

def update_filename(instance, filename):
    path = "uploads/images/"
    format = instance.username
    return os.path.join(path, format)

class Nationality(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Account(AbstractUser):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    Type = (
        ('P', 'Pilgrim'),
        ('V', 'Vendor'),
    )
    phone_number=models.BigIntegerField(null=True,blank=True)
    gender =models.CharField(max_length=1, choices=GENDER,null=True,blank=True)
    type =models.CharField(max_length=1, choices=Type,null=True,blank=True)
    image=models.ImageField(upload_to=update_filename, null=True,blank=True)
    nationality= models.ForeignKey(Nationality,on_delete=models.SET_NULL,null=True)
    stripe_account_id=models.CharField(max_length=250,blank=True,null=True)
    payment_confirm_pin=models.CharField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.first_name



class Role(Group):
    pass
