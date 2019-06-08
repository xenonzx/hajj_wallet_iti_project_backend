from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from vendors.models import Vendor
from vendors.api.serializers import VendorSerializer


from rest_framework.decorators import api_view


@api_view(['GET'])
def retrieve_nearest_vendors(request, format=None):
    if request.method == 'GET':
        lng = float(request.data['long'])
        lt = float(request.data['lat'])
        radius = request.data['radius']
        point = Point(lng,lt)
        print(point)
        data =Vendor.objects.filter(location=(point, Distance(km=radius)))
        serializer = VendorSerializer(data, many=True)

        return JsonResponse(serializer.data,safe=False)

