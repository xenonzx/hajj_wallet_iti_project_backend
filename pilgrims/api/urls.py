from django.contrib import admin
from django.urls import path ,include
from .views import NameRegistrationView
from .views import PilgrimDetailView

urlpatterns = [
    path('registration/pilgrims_register', NameRegistrationView.as_view(), name="rest_name_register"),
    path('<int:id>', PilgrimDetailView.as_view())
]


