from django.contrib import admin
from django.urls import path ,include
from .views import NameRegistrationView , TransactionsView,VendorDetailsView

urlpatterns = [
    path('registration/vendors_register', NameRegistrationView.as_view(), name="rest_name_register"),
    path('details', VendorDetailsView.as_view()),
    path('transactions', TransactionsView.as_view())

]


