from django.contrib import admin
from django.urls import path ,include
from .views import NameRegistrationView
from .views import PilgrimsDetailsView,PilgrimDetails
from .views import TransactionsView

urlpatterns = [
    path('registration/pilgrims_register', NameRegistrationView.as_view(), name="rest_name_register"),
    path('details', PilgrimsDetailsView.as_view()),
    path('transactions', TransactionsView.as_view()),
    path('viewdetails', PilgrimDetails.as_view()),
]


