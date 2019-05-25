from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_auth.registration.views import RegisterView
from .serializers import NameRegistrationSerializer,VendorSerializer
from pilgrims.models import Pilgrims
from rest_framework.response import Response
from vendors.models import Vendor
from accounts.models import Account
from rest_auth.views import LoginView

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



class CustomLoginView(LoginView):
  queryset = Vendor.objects.all()
  def get_response(self):
        orginal_response = super().get_response()
        account_details=Account.objects.filter(username=orginal_response.data['user']['username']).values('is_active','type','id')
        if account_details[0]['type'] == 'V':
          if account_details[0]['is_active']:
            vendor_details=Vendor.objects.filter(account_id=account_details[0]['id']).values('crn','code')
            mydata = {"vendor_details": vendor_details[0]}
        elif account_details[0]['type'] == 'P':
          mydata=''
        orginal_response.data.update(mydata)

        return orginal_response
