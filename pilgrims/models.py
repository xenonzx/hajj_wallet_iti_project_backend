from django.db import models
from accounts.models import Account

class Pilgrims(models.Model):
    account = models.ForeignKey(Account ,null=True ,blank=True,on_delete=models.CASCADE,related_name='pilgrim_account_id')
