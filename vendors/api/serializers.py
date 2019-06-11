from rest_framework import serializers
from vendors.models import Vendor
from rest_auth.models import TokenModel
from rest_auth.serializers import UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from accounts.models import Nationality,Account
from rest_framework.validators import UniqueValidator
# from rest_auth.serializers import UserDetailsSerializer
from vendors.models import Category
from payments.models import Transaction
from drf_extra_fields.geo_fields import PointField

class customUserDetailsSerializer(serializers.ModelSerializer):

  class Meta:
    model = Account
    fields = (
    'username', 'email', 'first_name', 'last_name', 'gender', 'phone_number', 'image', 'nationality')
    read_only_fields = ('email',)

  nationality = serializers.SerializerMethodField('get_nat_name')

  def get_nat_name(self, obj):
    return obj.nationality.name


class TokenSerializer(serializers.ModelSerializer):
  user = customUserDetailsSerializer(many=False, read_only=True)  # this is add by myself.

  class Meta:
    model = TokenModel
    fields = ('key', 'user')

class NameRegistrationSerializer(RegisterSerializer):

  email = serializers.CharField(required=True)
  username = serializers.CharField(required=True)
  first_name = serializers.CharField(required=True)
  last_name = serializers.CharField(required=True)
  phone_number = serializers.IntegerField(required=False)
  gender = serializers.CharField(required=True)
  image = serializers.ImageField(required=False)
  nationality = serializers.CharField(required=True)
  category = serializers.CharField(required=True)
  crn = serializers.IntegerField(required=True)
  code = serializers.CharField(required=True)
  location= serializers.CharField(required=True)

  type= serializers.CharField(required=False)


  def custom_signup(self, request, user):
    user.email = self.validated_data.get('email', '')
    user.username = self.validated_data.get('username', '')
    user.first_name = self.validated_data.get('first_name', '')
    user.last_name = self.validated_data.get('last_name', '')
    user.phone_number=self.validated_data.get('phone_number', '')
    user.gender = self.validated_data.get('gender', '')
    user.image = self.validated_data.get('image', '')
    user.type = 'V'
    nationality_obj = Nationality.objects.get(name=self.validated_data.get('nationality', ''))
    user.nationality = nationality_obj
    user.save(update_fields=['username','email','first_name','last_name', 'phone_number','type' ,'gender', 'image', 'nationality_id'])


    vendor =Vendor(account_id=user.pk)
    vendor.crn=self.validated_data.get('crn', '')
    vendor.code=self.validated_data.get('code', '')
    vendor.location=self.validated_data.get('location', '')
    category_obj = Category.objects.get(name=self.validated_data.get('category', ''))
    vendor.category = category_obj
    vendor.save()



# to display token with user details
class VendorSerializer(serializers.ModelSerializer):
  store_name = serializers.CharField(default='vendor.store_name')
  username = serializers.ReadOnlyField(source='account.username')
  first_name = serializers.ReadOnlyField(source='account.first_name',default='account.first_name')
  last_name = serializers.ReadOnlyField(source='account.last_name',default='account.last_name')
  email = serializers.ReadOnlyField(source='account.email',default='account.email',validators=[UniqueValidator(queryset=Account.objects.all())])
  phone_number = serializers.CharField(source='account.phone_number')
  gender = serializers.CharField(source='account.gender',default='account.gender')
  # type = serializers.CharField(source='account.type',default='account.type')
  image = serializers.CharField(source='account.image')
  code=serializers.CharField(default='vendor.code')
  lat = serializers.SerializerMethodField()
  long = serializers.SerializerMethodField()
  crn = serializers.IntegerField(default='vendor.crn')
  category=serializers.SerializerMethodField()
  nationality = serializers.SerializerMethodField()

  class Meta:
    model= Vendor
    fields=('store_name','username','email' ,'first_name', 'last_name','nationality','gender' ,'phone_number', 'crn',
            'code','category','image','lat','long')

  def get_nationality(self, obj):
    return obj.account.nationality.name

  def get_category(self, obj):
    return obj.category.name

  def get_lat(self, obj):
    return obj.location.x

  def get_long(self, obj):
    return obj.location.y

  def update(self, vendor, validated_data):
    vendor.account.phone_number = validated_data.get('phone_number', validated_data['account']['phone_number'])
    vendor.account.image = validated_data.get('image', validated_data['account']['image'])
    vendor.account.save()
    vendor.save()

    return vendor

class TransactionsSerializer(serializers.ModelSerializer):
    pilgrim_username = serializers.SerializerMethodField(read_only=True)
    pilgrim_phone = serializers.SerializerMethodField(read_only=True)
    pilgrim_id = serializers.SerializerMethodField()

    class Meta:
      model = Transaction
      fields = ['money_paid', 'time_stamp', 'pilgrim_username', 'pilgrim_phone', 'pilgrim_id']

    def get_pilgrim_username(self, obj):
      return obj.pilgrim.username

    def get_pilgrim_phone(self, obj):
      return obj.pilgrim.phone_number

    def get_pilgrim_id(self, obj):
      return obj.pilgrim.id

class FindVendorSerializer(serializers.Serializer):
  search_word = serializers.CharField(required=True)

class VendorSearchSerializer(serializers.Serializer):
  store_name=serializers.SerializerMethodField()
  store_id =serializers.SerializerMethodField()
  store_image = serializers.CharField(source='account.image')
  store_category=serializers.SerializerMethodField()

  class Meta:
    fields = ['store_name', 'store_id', 'store_image', 'store_category']

  def get_store_name(self,obj):
    return obj.store_name

  def get_store_id(self,obj):
    return obj.account.id

  def get_store_category(self,obj):
    return obj.category.name

class CategorySerializer(serializers.ModelSerializer):
  name=serializers.CharField()
  class Meta:
    model=Category
    fields=['name']
