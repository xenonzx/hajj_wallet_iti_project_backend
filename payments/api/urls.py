from django.urls import path
from .views import StripeCreateWallet ,StripeCheckWallet, StripeChargeWallet,\
        VendorCodeScan , StripePayVendor

urlpatterns = [
    path('create/', StripeCreateWallet.as_view()),
    path('exists/', StripeCheckWallet.as_view()),
    path('charge/', StripeChargeWallet.as_view()),
    path('vendor/scan/',VendorCodeScan.as_view()),
    path('vendor/pay/', StripePayVendor.as_view()),
]