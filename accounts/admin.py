# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Account

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Account
    list_display = ('username','email','first_name','last_name','is_staff')
    list_per_page = 6  # No of records per page

admin.site.register(Account, CustomUserAdmin)