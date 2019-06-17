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
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from accounts.models import Nationality



class NameRegistrationView(RegisterView):
  serializer_class = NameRegistrationSerializer
  queryset = Pilgrims.objects.all()

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    submitted_nationality= Nationality.objects.filter(name=request.data['nationality'])
    if len(submitted_nationality) is 0:
      return Response({'error':"invalid nationality"},status=status.HTTP_406_NOT_ACCEPTABLE)


    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    obj=Account.objects.filter(username=request.data.get('username'))
    id=(obj.values('id')[0]['id'])
    token = Token.objects.filter(user_id=id).values('key')[0]


    response_data = {
      "user": serializer.data,
      "token":token['key']
    }
    return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

@receiver(post_save, sender=Pilgrims)
def my_handler(sender, instance, created, **kwargs):
  if created:
    id = instance.account_id
    user = Account.objects.get(pk=id)
    user.is_active = True
    user.save()

class PilgrimsDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Pilgrims.objects.all()
    serializer_class = PilgrimSerializer
    def get_object(self):
      if(self.request.user.type != 'P'):
        raise NotFound(detail="you are not a pilgrim", code=404)
      else:
        return self.request.user

class PilgrimsDetail(generics.RetrieveAPIView):
  permission_classes = (IsAuthenticated,)
  def get(self,request,id):
    lookup_field = 'id'
    pilgrim = Account.objects.filter(id=id)
    if len(pilgrim) is 0:
      return Response({'error':'not found'},status=status.HTTP_404_NOT_FOUND)
    serializer_class = PilgrimSerializer
    serializer = PilgrimSerializer(pilgrim[0])
    return Response(serializer.data)

class PilgrimDetails(APIView):
  permission_classes = (IsAuthenticated,)
  queryset = Pilgrims.objects.all()
  serializer_class = PilgrimSerializer

  def post(self, request):
    pilgrim = Account.objects.filter(id=request.data['id'])

    serializer = PilgrimSerializer(pilgrim, many=True)
    return Response(serializer.data)

class TransactionsView(APIView):
  permission_classes = (IsAuthenticated,)

  def get(self, request, format=None):
    transactions = Transaction.objects.select_related('vendor').filter(pilgrim_id=request.user.id)
    if len(transactions)>0:
      serializer = TransactionsSerializer(transactions, many=True , context={'request': request})
      return Response(serializer.data)
    raise NotFound(detail="pilgrim with no transactions",code=404)

