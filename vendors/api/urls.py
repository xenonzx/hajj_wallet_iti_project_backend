from django.contrib import admin
from django.urls import path ,include
from .views import NameRegistrationView , TransactionsView,VendorDetailsView,VendorsDetails,\
    CategoryList, FindVendorView

urlpatterns = [
    path('registration/vendors_register', NameRegistrationView.as_view(), name="rest_name_register"),
    path('details', VendorDetailsView.as_view()),
    path('find', FindVendorView.as_view()),
    path('viewdetails', VendorsDetails.as_view()),
    path('transactions', TransactionsView.as_view()),
    path('categories', CategoryList.as_view())

]


