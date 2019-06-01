from django.conf.urls import url
from .views import retrieve_nearest_vendors



urlpatterns = [
    url('nearest_vendors', retrieve_nearest_vendors),

]