from rest_framework import generics,status
from accounts.models import Account
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_auth.registration.views import RegisterView
from .serializers import NameRegistrationSerializer,PilgrimSerializer , TransactionsSerializer
from pilgrims.models import Pilgrims
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from payments.models import Transaction
from rest_framework.exceptions import NotFound


class NameRegistrationView(RegisterView):
  serializer_class = NameRegistrationSerializer
  queryset = Pilgrims.objects.all()

  def create(self, request, *args, **kwargs):
    print(request.data)
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    obj=Account.objects.filter(username=request.data.get('username'))
    id=(obj.values('id')[0]['id'])
    token = Token.objects.filter(user_id=id).values('key')[0]

    # Define how would you like your response data to look like.
    response_data = {
      "user": serializer.data,
      "token":token
    }
    return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class PilgrimDetailView(generics.RetrieveUpdateAPIView):
  lookup_field = 'id'
  queryset = Pilgrims.objects.all()
  serializer_class = PilgrimSerializer

  def user_update(request, pk):
    pilgrim = Pilgrims.objects.get(id=pk)
    if request.method == "PUT":
      serializer = PilgrimSerializer(pilgrim, data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      else:
        return Response({"error": serializer.errors, "error": True})
    serializer = PilgrimSerializer(pilgrim)
    return Response(serializer.data)

class TransactionsView(APIView):
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    transactions = Transaction.objects.all()
    if len(transactions)>0:
      serializer = TransactionsSerializer(transactions, many=True)
      return Response(serializer.data)
    raise NotFound(detail="pilgrim with no transactions",code=404)