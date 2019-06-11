"""hajwallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include
from vendors.api.views import CustomLoginView
from rest_auth.views import PasswordResetConfirmView,PasswordResetView
from custom_admin.admin import admin_site


urlpatterns = [
    path('admin/', admin_site.urls),
    path('rest_auth/', include('rest_auth.urls')),
    path('rest_auth/registration/', include('rest_auth.registration.urls')),
    path('pilgrims/', include('pilgrims.api.urls')),
    path('vendors/', include('vendors.api.urls')),
    path('custom/login/', CustomLoginView.as_view(), name='my_custom_login'),
    path('rest_auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url('statistics/', include('statistics_app.urls')),
    url('search/', include('search.urls')),
    url('accounts/',include('accounts.api.urls')),
    path('wallet/', include('payments.api.urls')),



]
