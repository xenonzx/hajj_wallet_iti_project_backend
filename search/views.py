from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from django.contrib.gis.geos import Point
from vendors.models import Vendor
from vendors.api.serializers import VendorSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


# @api_view(['GET'])
class Search(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        if request.method == 'GET':
            lng = float(request.data['long'])
            lt = float(request.data['lat'])
            radius = request.data['radius']
            category = int(request.data['category'])
            point = Point(lng,lt)
            print(point)
            if category =='':
                data =Vendor.objects.filter(location__distance_lt=(point, radius))
            else:
                data = Vendor.objects.filter(location__distance_lt=(point, radius),category_id = category)


            serializer = VendorSerializer(data, many=True)

            return JsonResponse(serializer.data,safe=False)

