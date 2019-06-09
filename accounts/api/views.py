from accounts.api.serializers import NationalitySerializer
from rest_framework import generics
from rest_framework.response import Response

from accounts.models import Nationality,Account

class NationalityList(generics.ListAPIView):
    queryset=Nationality.objects.all()
    serializer_class= NationalitySerializer

    def list(self, request):
        queryset=self.get_queryset()
        serializer=NationalitySerializer(queryset, many=True)
        return Response(serializer.data)
