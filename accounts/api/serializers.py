from rest_framework import serializers
from accounts.models import Nationality,Account

class NationalitySerializer(serializers.ModelSerializer):
  name= serializers.CharField()
  class Meta:
    model= Nationality
    fields=['name']
