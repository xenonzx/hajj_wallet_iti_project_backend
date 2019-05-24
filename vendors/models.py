from django.contrib.gis.db import models
from accounts.models import Account
from django.contrib.auth.models import User

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
    # user = models.OneToOneField(User)

    def __str__(self):
        return self.account.username

    def __str__(self):
        return self.account.username

    def view_vendor_name(self):
        return self.account.first_name + " " + self.account.last_name

    view_vendor_name.shortDescription = "Vendor Name"

    def view_vendor_nationality(self):
        return self.account.nationality

    def view_vendor_email(self):
        return self.account.email

    def view_vendor_image(self):
        return self.account.image

    def view_vendor_username(self):
        return self.account.username

    def view_vendor_phone_number(self):
        return self.account.phone_number

    def view_vendor_category(self):
        return self.category.name


