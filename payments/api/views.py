import stripe
import time
import hashlib
import math
from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from vendors.models import Vendor
from accounts.models import Account
from payments.models import Transaction
from rest_framework.response import Response
from .serializers import WalletCreateSerializer,WalletChargeSerializer ,\
  VendorScanSerializer , VendorConfirmSerializer ,VendorPaySerializer

class StripePayVendor(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self,request,format=None):
    data = request.data
    current_user = request.user
    error={'error':'an error has occurred'}
    data_validate = VendorPaySerializer(data=data)
    data_validate.is_valid(raise_exception=True)

    vendor = Account.objects.filter(id=data['vendor_id'])
    if len(vendor) == 0:
      return Response(error,status=status.HTTP_400_BAD_REQUEST)
    pin_entered = hash_pin_code(data['pin_code'])
    pin_stored = current_user.payment_confirm_pin
    if pin_entered != pin_stored:
      return Response(error,status=status.HTTP_406_NOT_ACCEPTABLE)

    if current_user.stripe_account_id is None or vendor[0].stripe_account_id is None:
      return Response(error,status=status.HTTP_400_BAD_REQUEST)

    current_user_balance = get_stripe_balance(current_user)
    if current_user_balance < int(data['amount']):
      return Response(error,status=status.HTTP_406_NOT_ACCEPTABLE)

    charge=charge_user_wallet(data['amount'],data['currency'],current_user.stripe_account_id)
    if charge:
      amount_to_charge = calculate_fund_after_paying(data['amount'])
      transfer=transfer_to_wallet(amount_to_charge,data['currency'],vendor[0].stripe_account_id,charge['id'])
      if transfer:
        transaction_processed = Transaction(money_paid=int(data['amount']),pilgrim_id=current_user.id,
                                     vendor_id=vendor[0].id,time_stamp=datetime.now())
        transaction_processed.save()
        return Response({'success':'transaction processed successfully'},status=status.HTTP_202_ACCEPTED)
    return Response(error,status=status.HTTP_406_NOT_ACCEPTABLE)


class VendorCodeScan(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self,request,format=None):
    data = request.data
    data_validate = VendorScanSerializer(data=data)
    data_validate.is_valid(raise_exception=True)
    vendor = Vendor.objects.select_related('account').filter(code=data['code'])
    if len(vendor)==0: ## vendor not found
      return Response({'error':'vendor not found'},status=status.HTTP_400_BAD_REQUEST)
    serialized_vendor=VendorConfirmSerializer(vendor[0])
    return Response(serialized_vendor.data)

class StripeChargeWallet(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self,request,format=None):
    data = request.data
    user = request.user
    data_validate=WalletChargeSerializer(data=data)
    data_validate.is_valid(raise_exception=True)
    pin_entered=hash_pin_code(data['pin_code'])
    pin_stored = user.payment_confirm_pin
    if pin_entered != pin_stored:
      return Response({'error':'an error has occurred'},
                      status=status.HTTP_406_NOT_ACCEPTABLE)

    token = generate_card_token(data['card_number'],data['exp_month'],
                                data['exp_year'],data['cvc'])
    if token:
      charge = charge_user_card(data['amount'],data['currency'],token)
      if charge:
        amount_to_charge = calculate_fund_after_recharge(data['amount'])
        transfer = transfer_to_wallet(amount_to_charge,data['currency'],
                         user.stripe_account_id,charge['id'])
        if transfer:
          return Response({'success': 'account charged successfully'},
                        status=status.HTTP_202_ACCEPTED)
      return Response({'error':'an error has occurred'},
                      status=status.HTTP_409_CONFLICT)

class StripeCheckWallet(APIView):
  permission_classes = (IsAuthenticated,)
  def get(self,request , format=None):
    current_user=request.user
    if current_user.stripe_account_id is None:
      return Response({"error": "user doesn't have wallet"}, status=status.HTTP_204_NO_CONTENT)
    total_balance = get_stripe_balance(current_user)
    return Response({"success":{
              "total_balance": total_balance
      }},status=status.HTTP_200_OK)

class StripeCreateWallet(APIView):
  permission_classes = (IsAuthenticated,)
  def post(self , request , format=None):
    data = request.data
    data_validate = WalletCreateSerializer(data=data)
    data_validate.is_valid(raise_exception=True)
    self.create_custom_account(data,request.user)
    return Response({"success": "wallet created successfully"}, status=status.HTTP_200_OK)

  def create_custom_account(self,data,user):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    account = stripe.Account.create(
      country=data['country'],
      type='custom',
      business_type='individual',
      requested_capabilities=['platform_payments'],  # provide credit card to platform
      external_account=  # creating bank account
      {
        'object': 'bank_account',
        'bank_name': data['bank_name'],
        'country': data['country'],
        'currency': data['currency'],
        'account_number': data['account_number'],
        'routing_number': data['routing_number'],
      },
      individual={  ## required personal data for account
        'first_name': user.first_name or 'no_first',
        'last_name': user.type or 'no_last',
        'ssn_last_4': data['ssn_last_numbers'],
        'dob': {
          'day': data['dob_day'],
          'month': data['dob_month'],
          'year': data['dob_year'],
        }
      },
      settings={  ### setting payout to manual
        'payouts': {
          'schedule': {
            'interval': 'manual'
          }
        }
      },
      business_profile={  ## business required data even for individual accounts
        'product_description': 'we are testing connect',
        'url': 'https://testconnecturl.com'
      },
      tos_acceptance={  # terms of service
        'date': int(time.time()),
        'ip': '8.8.8.8',
      },

    )
    if account:
      user.stripe_account_id = account['id']
      user.payment_confirm_pin = hash_pin_code(data['pin_code'])
      user.save()


def hash_pin_code(pin_code):
    pin_code.replace(" ","")
    encoded_bin = pin_code.encode('utf-8')
    hashed_pin_code=hashlib.sha512(encoded_bin).hexdigest()
    return hashed_pin_code

def charge_user_wallet(amount,currency,user_stripe_id):
  stripe.api_key = settings.STRIPE_SECRET_KEY
  charge = stripe.Charge.create(
    amount= amount,
    currency= currency,
    source= user_stripe_id
  )
  return charge


def transfer_to_wallet(amount,currency,user_stripe_id,charge_id):
  stripe.api_key = settings.STRIPE_SECRET_KEY
  transfer = stripe.Transfer.create(
    amount=amount,
    currency=currency,
    destination= user_stripe_id,
  )
  return transfer

def charge_user_card(amount,currency,token):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    charge = stripe.Charge.create(
      amount=amount,
      currency= currency,
      source=token,
    )
    return charge

def get_stripe_balance(current_user):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    balance = stripe.Balance.retrieve(
      stripe_account= current_user.stripe_account_id
    )
    print(balance)
    return balance['available'][0]['amount'] ## return pending money for testing accounts


def generate_card_token(card_number,exp_month,exp_year,cvc):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    key = stripe.Token.create(
      card={
        'number': card_number,
        'exp_month': exp_month,
        'exp_year': exp_year,
        'cvc': cvc,
      },
    )
    return key

def calculate_fund_after_recharge(charged_amount):
  amount_to_charge = math.floor(int(charged_amount) * 0.98)
  return str(amount_to_charge)

def calculate_fund_after_paying(transferred_amount):
  amount_to_charge = math.floor(int(transferred_amount)*0.97)
  return str(amount_to_charge)
