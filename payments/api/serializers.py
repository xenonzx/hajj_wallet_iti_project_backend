from rest_framework import serializers
from vendors.models import Vendor

class VendorPaySerializer(serializers.Serializer):
    vendor_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    pin_code= serializers.IntegerField()
    currency = serializers.CharField()

class VendorScanSerializer(serializers.Serializer):
    code = serializers.CharField()

class VendorConfirmSerializer(serializers.ModelSerializer):
    store_name = serializers.SerializerMethodField()
    store_image = serializers.CharField(source='account.image')
    store_id = serializers.SerializerMethodField()
    store_username= serializers.SerializerMethodField()
    store_category= serializers.SerializerMethodField()

    class Meta:
        model= Vendor
        fields=('store_name','store_image','store_id','store_username','store_category')

    def get_store_name(self,obj):
        return obj.store_name
    def get_store_id(self,obj):
        return obj.account.id
    def get_store_username(self,obj):
        return obj.account.username
    def get_store_category(self,obj):
        return obj.category.name

class WalletChargeSerializer(serializers.Serializer):
    card_number = serializers.IntegerField()
    exp_month = serializers.IntegerField()
    exp_year = serializers.IntegerField()
    cvc = serializers.IntegerField()
    amount = serializers.IntegerField()
    currency =serializers.CharField()
    pin_code= serializers.IntegerField()

class WalletCreateSerializer(serializers.Serializer):
    country = serializers.CharField(max_length=100)
    bank_name = serializers.CharField(max_length=100)
    account_number = serializers.IntegerField()
    routing_number = serializers.IntegerField()
    currency = serializers.CharField()
    dob_day = serializers.IntegerField()
    dob_month = serializers.IntegerField()
    dob_year = serializers.IntegerField()
    ssn_last_numbers = serializers.IntegerField()
    pin_code = serializers.IntegerField()
