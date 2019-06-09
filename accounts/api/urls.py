from django.urls import path, include
from accounts.api.views import NationalityList

urlpatterns = [
    path('nationalities', NationalityList.as_view())
]
