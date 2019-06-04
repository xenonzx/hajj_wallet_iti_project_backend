from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_auth.registration.views import RegisterView
from .serializers import NameRegistrationSerializer, TransactionsSerializer,VendorSerializer
from pilgrims.models import Pilgrims
from rest_framework.response import Response
from vendors.models import Vendor
from accounts.models import Account
from rest_auth.views import LoginView
from rest_framework.views import APIView
from payments.models import Transaction
from rest_framework.exceptions import NotFound
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.contrib.gis.geos import GEOSGeometry


class NameRegistrationView(RegisterView):
  queryset = Vendor.objects.all()
  serializer_class = NameRegistrationSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)

    response_data = {
      "message": "waiting for approved",
    }
    return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class VendorDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    def get_object(self):
        if (self.request.user.type != 'V'):
            raise NotFound(detail="you are not a vendor", code=404)
        else:
            acc=Account.objects.get(email=self.request.user.email)
            vendor=Vendor.objects.get(account_id=acc.id)
            return vendor


@receiver(post_save, sender=Account)
def my_handler(sender, instance,created, **kwargs):

    if created:
        id = instance.id
        user = Account.objects.get(pk=id)
        user.is_active=False
        user.save()

class CustomLoginView(LoginView):
  queryset = Vendor.objects.all()
  def get_response(self):
        orginal_response = super().get_response()
        account_details=Account.objects.filter(username=orginal_response.data['user']['username']).values('is_active','type','id')
        if account_details[0]['type'] == 'V':
          if account_details[0]['is_active']:
            vendor_details=Vendor.objects.filter(account_id=account_details[0]['id']).values('crn','code','lat','long')
            mydata = {"vendor_details": vendor_details[0]}

        elif account_details[0]['type'] == 'P':
          mydata=''
        orginal_response.data.update(mydata)

        return orginal_response

class TransactionsView(APIView):
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    transactions = Transaction.objects.select_related('pilgrim').filter(vendor_id=request.user.id)
    if len(transactions)>0:
      serializer = TransactionsSerializer(transactions, many=True , context={'request': request})
      return Response(serializer.data)
    raise NotFound(detail=" Vendor with no transactions",code=404)

