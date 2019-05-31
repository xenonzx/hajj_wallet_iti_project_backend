from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from pilgrims.models import Pilgrims
from django.db.models import Count
from vendors.models import Vendor
from payments.models import Transaction
from django.db.models.functions import Concat
from django.db.models import Value as V
from rest_framework.decorators import authentication_classes, permission_classes

import datetime

# Create your views here.


class Charts(viewsets.ViewSet):

    @authentication_classes([])
    @permission_classes([])
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


    def best_vendors(self, request, format=None):
        from_date = datetime.datetime.now() - datetime.timedelta(days=7)

        statis = Transaction.objects.filter(time_stamp__range=[from_date, datetime.datetime.now()]).prefetch_related('vendor') \
            .prefetch_related('vendor__account') \
            .filter(vendor__nationality_id__isnull=False) \
            .annotate(dcount=Count('vendor__first_name'),full_name=Concat('vendor__first_name',V(' '),'vendor__last_name'))\
            .order_by('-dcount')
        labels = statis.values_list('full_name', flat=True)
        defult_items = statis.values_list('dcount', flat=True)
        data = {
            "labels": labels,
            "defult": defult_items,
        }

        return Response(data)

    def most_active_users(self, request, format=None):
        from_date = datetime.datetime.now() - datetime.timedelta(days=7)

        statis = Transaction.objects.filter(time_stamp__range=[from_date, datetime.datetime.now()]).prefetch_related('pilgrim')\
            .prefetch_related('pilgrim__account') \
            .filter(pilgrim__nationality_id__isnull=False) \
            .annotate(dcount=Count('pilgrim__first_name'),full_name=Concat('pilgrim__first_name',V(' '),'pilgrim__last_name'))\
            .order_by('-dcount')
        labels = statis.values_list('full_name', flat=True)
        defult_items = statis.values_list('dcount', flat=True)
        data = {
            "labels": labels,
            "defult": defult_items,
        }

        return Response(data)
