from django.contrib.gis.db import models
from accounts.models import Account

class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()

    def __str__(self):
        return self.name

class Vendor(models.Model):
    account = models.ForeignKey(Account,null=True,blank=True,on_delete=models.CASCADE,related_name='vendor_account_id')
    crn=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    location = models.PointField()
    code=models.CharField(max_length=250)

    def __str__(self):
        return self.crn

