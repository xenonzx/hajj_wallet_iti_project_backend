from django.conf.urls import url
from .views import Charts


urlpatterns = [
    url('chart/pilgrims_ratio', Charts.as_view({'get': 'retrieve_pilgrims_ratio'})),
    url('chart/vendors_categories', Charts.as_view({'get': 'retrieve_vendors_categories'})),
    url('chart/best_vendors', Charts.as_view({'get': 'best_vendors'})),
    url('chart/most_active_users', Charts.as_view({'get': 'most_active_users'})),

]