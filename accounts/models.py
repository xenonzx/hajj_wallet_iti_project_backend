from django.db import models
from django.contrib.auth.models import AbstractUser
import os

def update_filename(instance, filename):
    path = "uploads/images/"
    format = instance.username
    return os.path.join(path, format)

class Nationality(models.Model):
    name=models.CharField(max_length=50)

class Account(AbstractUser):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    Type = (
        ('P', 'Pilfrim'),
        ('V', 'Vendor'),
    )
    phone_number=models.IntegerField(null=True,blank=True)
    gender =models.CharField(max_length=1, choices=GENDER,null=True,blank=True)
    type =models.CharField(max_length=1, choices=Type,null=True,blank=True)
    image=models.ImageField(upload_to=update_filename, null=True,blank=True)
    nationality= models.ForeignKey(Nationality,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.first_name

