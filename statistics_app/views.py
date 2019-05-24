from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from pilgrims.models import Pilgrims
from django.db.models import Count
from vendors.models import Vendor

# Create your views here.


class Charts(viewsets.ViewSet):

    def retrieve_pilgrims_ratio(self, request, format=None):

        statis = Pilgrims.objects.prefetch_related('account').filter(account__nationality_id__isnull=False) \
            .prefetch_related('account__nationality').filter(
            account__is_staff=0).values(
            'account__nationality__name') \
            .annotate(dcount=Count('account__nationality__name'))

        labels = statis.values_list('account__nationality__name', flat=True)
        defult_items = statis.values_list('dcount', flat=True)
        data = {
            "labels":labels,
            "defult":defult_items,
        }
        return Response(data)


    def retrieve_vendors_categories(self, request, format=None):
        statis = Vendor.objects.prefetch_related('category').values(
            'category__name') \
            .annotate(dcount=Count('category__name'))


        labels = statis.values_list('category__name', flat=True)
        defult_items = statis.values_list('dcount', flat=True)
        data = {
            "labels":labels,
            "defult":defult_items,
        }
        return Response(data)