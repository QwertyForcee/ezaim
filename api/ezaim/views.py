from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
import jwt
import json
import bcrypt
#
import pprint
from decimal import *

from api.settings import JWT_KEY
from ezaim.utils import JWTAuthentication
from ezaim.utils import WebpayCurrency, pay_loan, get_loan
from django.views.decorators.csrf import csrf_exempt



from ezaim.models import (
    User, TelegramUser, UserSettings,
    PassportData, Address,
    PaymentCard, Payment, Loan, 
    Currency, Log
)
from ezaim.serializers import (
    CurrencySerializer,
    UserSerializer,
    AddressSerializer, 
    PassportDataSerializer,
    UserSettingsSerializer,
    TelegramUserSerializer,
    PaymentCardSerializer,
    LoanSerializer,
    PaymentSerializer,
    LogSerializer
)


def not_found(request, *args, **kwargs):
    return JsonResponse(data={"message": "Not Found"}, status=404)

def app_error(request, *args, **kwargs):
    return JsonResponse(data={"message": "Server Error"}, status=500)

def not_authorized(request, *args, **kwargs):
    return JsonResponse(data={"message": "Unauthorized"}, status=401)

@csrf_exempt
def test_pay(request):
    resp = pay_loan(
        "order-test", 
        1, 
        WebpayCurrency.BYN,
        "100",
        "customer-test",
        "http://127.0.0.1:8000/admin"
    )
    return JsonResponse(resp)

@csrf_exempt
def test_loan(request):
    resp = None
    JsonResponse(resp)

@csrf_exempt
def login(request: HttpRequest, *args, **kwargs):
    data = json.loads(request.body.decode())
    email, password = data['email'], data['password']

    try:
        user = User.objects.get(email=email)
        hashed = bcrypt.hashpw(password, user.salt)
        if not bcrypt.checkpw(user.password, hashed):
            return not_authorized(request)
    except ObjectDoesNotExist:
        return not_found(request)
    except MultipleObjectsReturned:
        return app_error(request)
    token = jwt.encode(
        {
            "id": user.pk
        }, 
        JWT_KEY, 
        algorithm='HS256'
    )
    return JsonResponse({
        "access_token": token
    })

def parse_address(address) -> Address:
    country = address.get('country', None)
    state = address.get('state', None)
    city = address.get('city', None) 
    code_soato = address.get('codeSoato', None)
    street = address.get('street', None)
    house = address.get('house', None)
    flat = address.get('flat', None)
    mail_index = address.get('mailIndex', None)
    return Address(
        country=country,
        state=state,
        city=city,
        code_soato=code_soato,
        street=street,
        house=house,
        flat=flat,
        mail_index=mail_index
    )

@csrf_exempt
def signup(request: HttpRequest, *args, **kwargs):
    data = json.loads(request.body.decode())

    email = data.get('email', None)
    password = data.get('password', None)
    phone_number = data.get('phoneNumber', None)
    password = data.get('password', None)
    salary = data.get('salary', None)

    name = data.get('name', None)
    surname = data.get('surname', None)
    passport_number = data.get('passportNumber', None)
    identification_number = data.get('identificationNumber', None)
    issue_date = data.get('issueDate', None)
    expiry_date = data.get('expiryDate', None)
    authority = data.get('authority', None)
    nationality = data.get('nationality', None)

    sex = data.get('sex', None)
    resident = data.get('resident', None)
    birth_date = data.get('birthDate', None)

    if salary is None:
        salary = Decimal()

    try:
        # birth_address = parse_address(data['birthAddress'])
        registration_address = parse_address(data['registrationAddress'])
        registration_address.save()
        print('reg add saved')
        residential_address = parse_address(data['residentialAddress'])
        residential_address.save()
        print('res add saved')
    except Exception:
        print('something went wrong')


    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    user = User(
        email=email,
        password=hashed,
        salt=salt,
        phone_number=phone_number,
        salary=salary,
        name=name,
        surname=surname
    )
    user.save()
    print('user saved')
    user_settings = UserSettings(
        user=user
    )
    user_settings.save()
    print('user settings saved')

    passport = PassportData(
        user=user,
        name=name,
        surname=surname,
        passport_number=passport_number,
        identification_number=identification_number,
        issue_date=issue_date,
        expiry_date=expiry_date,
        authority=authority,
        nationality=nationality,
        sex=sex,
        resident=resident,
        birth_date=birth_date,
        birth_country=data['birthAddress']['country'],
        birth_state=data['birthAddress']['state'],
        birth_city=data['birthAddress']['city'],
        registration_address=registration_address,
        residential_address=residential_address
    )
    passport.save()
    print('passport saved')

    token = jwt.encode(
        {
            "id": user.pk
        }, 
        JWT_KEY, 
        algorithm='HS256'
    )
    return JsonResponse({
        "access_token": token
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class UserSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSettingsSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserSettings.objects.filter(user_id=self.request.user)

class TelegramUsersViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserSettings.objects.filter(user_id=self.request.user)

class LoanViewSet(
        viewsets.GenericViewSet, 
        mixins.ListModelMixin, 
        mixins.CreateModelMixin, 
        mixins.RetrieveModelMixin):
    serializer_class = LoanSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        print('loan viewset: perform create')
        data = json.loads(self.request.body.decode())
        serializer.save(
            user = self.request.user
            # remaining_amount = data['remaining_amount']
        )
        return super().perform_create(serializer)

class PaymentViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin):
    serializer_class = PaymentSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Payment.objects.filter(loan_id__user=self.request.user)

    def perform_create(self, serializer):
        print('payment viewset: perform create')
        return super().perform_create(serializer)

class PaymentCardViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentCardSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PaymentCard.objects.filter(owner_id=self.request.user)