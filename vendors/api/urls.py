from django.contrib import admin
from django.urls import path ,include
from .views import NameRegistrationView , TransactionsView

urlpatterns = [
    path('registration/vendors_register', NameRegistrationView.as_view(), name="rest_name_register"),
    path('transactions', TransactionsView.as_view())

]


