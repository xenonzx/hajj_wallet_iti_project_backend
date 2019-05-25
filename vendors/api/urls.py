from django.contrib import admin
from django.urls import path ,include
from .views import NameRegistrationView


urlpatterns = [
    path('registration/vendors_register', NameRegistrationView.as_view(), name="rest_name_register"),

]


