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

  first_name = serializers.CharField(required=False)
  last_name = serializers.CharField(required=False)
  phone_number = serializers.IntegerField(required=False)
  gender = serializers.CharField(required=False)
  image = serializers.ImageField(required=False)
  nationality = serializers.CharField(required=True)
  type = serializers.CharField(required=False)

  def custom_signup(self, request, user):
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.phone_number=self.validated_data.get('phone_number', '')
    user.gender = self.validated_data.get('gender', '')
    user.image = self.validated_data.get('image', '')
    user.type='P'
    nationality_obj = Nationality.objects.get(name=self.validated_data.get('nationality', ''))
    user.nationality = nationality_obj
    user.save(update_fields=['first_name', 'last_name','type' ,'phone_number', 'gender', 'image', 'nationality_id'])
    pilgrim =Pilgrims(account_id=user.pk)
    pilgrim.save()



class PilgrimSerializer(serializers.ModelSerializer):
  username = serializers.ReadOnlyField(source='account.username')
  first_name = serializers.ReadOnlyField(source='account.first_name')
  last_name = serializers.ReadOnlyField(source='account.last_name')
  email = serializers.CharField(source='account.email',validators=[UniqueValidator(queryset=Account.objects.all())])
  phone_number = serializers.CharField(source='account.phone_number')
  gender = serializers.CharField(source='account.gender')
  image = serializers.CharField(source='account.image')

  class Meta:
    model= Pilgrims
    fields=['username','email' ,'first_name', 'last_name', 'phone_number', 'gender', 'image']




  def update(self, pilgrim, validated_data):

    pilgrim.account.email = validated_data.get('email', validated_data['account']['email'])
    pilgrim.account.phone_number = validated_data.get('phone_number', validated_data['account']['phone_number'])
    pilgrim.account.gender = validated_data.get('gender', validated_data['account']['gender'])
    pilgrim.account.image = validated_data.get('image', validated_data['account']['image'])
    pilgrim.account.save()

    return pilgrim

  class TransactionsSerializer(serializers.ModelSerializer):
    vendor_username= serializers.SerializerMethodField('get_vendor_username')
    vendor_phone=serializers.SerializerMethodField('get_vendor_phone')

    class Meta:
      model = Transaction
      fields=['money_paid','time_stamp','vendor_username','vendor_phone']

    def get_vendor_username(self,obj):
      return obj.vendor_id.username

    def get_vendor_phone(self,obj):
      return obj.vendor_id.phone_number