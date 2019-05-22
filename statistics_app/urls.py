from django.conf.urls import url
from .views import Charts


urlpatterns = [
    url('chart/pilgrims_ratio', Charts.as_view({'get': 'retrieve_pilgrims_ratio'})),
    url('chart/vendors_categories', Charts.as_view({'get': 'retrieve_vendors_categories'})),

]