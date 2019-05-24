# users/admin.py
from django.contrib import admin
from custom_admin.admin import admin_site
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Account,Nationality


class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Account
    list_display = ('username','email','first_name','last_name','is_staff')
    list_filter = ('is_staff',)

    list_per_page = 6  # No of records per page

    def get_queryset(self, request):
        qs = Account.objects.filter(is_staff=1)
        return qs

class NationalityAdmin(admin.ModelAdmin):

    list_per_page = 6

    list_display = ('name',)

    list_filter = ('name',)

    search_fields = ['name',]


admin_site.register(Account, CustomUserAdmin)
admin_site.register(Nationality, NationalityAdmin)