from django.conf.urls import url
# from .views import retrieve_nearest_vendors
from django.urls import path
from .views import Search


urlpatterns = [
    # url('nearest_vendors', retrieve_nearest_vendors),
    # url('nearest_vendors', search.as_view()),
    path('nearest_vendors', Search.as_view()),
]