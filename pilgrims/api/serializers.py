from rest_framework import serializers
from pilgrims.models import Pilgrims
from rest_auth.models import TokenModel
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from accounts.models import Nationality,Account
from rest_framework.validators import UniqueValidator
from rest_auth.serializers import UserDetailsSerializer
from rest_framework.authtoken.models import Token
from payments.models import Transaction

class NameRegistrationSerializer(RegisterSerializer):

  email = serializers.CharField(required=True)
  username = serializers.CharField(required=True)
  first_name = serializers.CharField(required=True)
  last_name = serializers.CharField(required=True)
  phone_number = serializers.CharField(required=False)
  gender = serializers.CharField(required=True)
  image = serializers.CharField(required=False)
  nationality = serializers.CharField(required=True)
  type = serializers.ReadOnlyField(required=False)

  def custom_signup(self, request, user):
    user.email = self.validated_data.get('email', '')
    user.username = self.validated_data.get('username', '')
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.phone_number=self.validated_data.get('phone_number', )
    user.gender = self.validated_data.get('gender', '')
    user.image = self.validated_data.get('image', '')
    user.type='P'
    nationality_obj = Nationality.objects.get(name=self.validated_data.get('nationality', ''))
    user.nationality = nationality_obj

    user.save(update_fields=['username','email','first_name', 'last_name','type' ,'phone_number', 'gender', 'image', 'nationality_id'])
    pilgrim =Pilgrims(account_id=user.pk)
    pilgrim.save()



class PilgrimSerializer(serializers.ModelSerializer):
  username = serializers.ReadOnlyField()
  first_name = serializers.ReadOnlyField()
  last_name = serializers.ReadOnlyField()
  email = serializers.ReadOnlyField()
  phone_number = serializers.CharField()
  gender = serializers.CharField()
  image = serializers.CharField()
  class Meta:
    model= Pilgrims
    fields=['username','email' ,'first_name', 'last_name', 'phone_number', 'gender', 'image']


  def update(self, pilgrim, validated_data):
    pilgrim.phone_number = validated_data.get('phone_number', validated_data['phone_number'])
    pilgrim.image = validated_data.get('image', validated_data['image'])
    pilgrim.save()
    return pilgrim

class TransactionsSerializer(serializers.ModelSerializer):

    vendor_username= serializers.SerializerMethodField(read_only=True)
    vendor_phone= serializers.SerializerMethodField(read_only=True)
    vendor_id = serializers.SerializerMethodField()

    class Meta:
      model = Transaction
      fields=['money_paid','time_stamp','vendor_username','vendor_phone','vendor_id']

    def get_vendor_username(self,obj):
      return obj.vendor.username

    def get_vendor_phone(self,obj):
      return obj.vendor.phone_number

    def get_vendor_id(self,obj):
      return obj.vendor.id




