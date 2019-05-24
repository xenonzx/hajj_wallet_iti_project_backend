from django.db import models

from django.contrib import admin
from accounts.models import Account

class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        # top6 = Account.objects.order_by('id')[:6]
        context = {'top6': '2'}
        if extra_context is None:
            extra_context = {context}
        return super(MyAdminSite, self).index(request, extra_context)
