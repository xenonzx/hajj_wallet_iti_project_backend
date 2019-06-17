from django.db import models
from accounts.models import Account
class Transaction(models.Model):
    pilgrim=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,related_name='pilgrim_id')
    vendor=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True,related_name='vendor_id')
    money_paid=models.IntegerField()
    time_stamp=models.DateTimeField()

