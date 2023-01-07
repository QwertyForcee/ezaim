from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import jwt
import json
import bcrypt
from pprint import pprint

from users.utils import JWTAuthentication
from users.models import (
    Log,
    Address,
    User,
    PassportData,
    TelegramUser,
    UserSettings
)
from loans.models import (
    Currency
)
from users.serializers import *
from api.settings import JWT_KEY

def not_found():
    return JsonResponse(data={"message": "Not Found"}, status=404)

def app_error():
    return JsonResponse(data={"message": "Server Error"}, status=500)

def not_authorized():
    return JsonResponse(data={"message": "Unauthorized"}, status=401)

def bad_request(message):
    return JsonResponse(data={"message": f'Bad Request: {message}'}, status=400)

@csrf_exempt
def login(request: HttpRequest, *args, **kwargs):
    data = json.loads(request.body.decode())
    email, password = data['email'], data['password']
    # pprint(data)

    try:
        user = User.objects.filter(email=email).first()
        hashed = bcrypt.hashpw(password.encode(), user.salt)
        if user.password != hashed:
            return not_authorized()
    except ObjectDoesNotExist:
        return not_found()
    except MultipleObjectsReturned:
        return app_error()
    token = jwt.encode(
        {
            "id": user.pk
        }, 
        JWT_KEY, 
        algorithm='HS256'
    )
    log = Log(
        log=f'{email} logged in'
    )
    log.save()
    return JsonResponse({
        "access_token": token
    })


def parse_address(address) -> Address:
    address_data_fields = (
        'country', 'state', 'city',
        'codeSoato', 'street', 'house',
        'flat', 'mailIndex'
    )
    address_data = {}
    for data_field in address_data_fields:
        address_data[data_field] = address[data_field]

    return Address(
        country=address_data['country'],
        state=address_data['state'],
        city=address_data['city'],
        code_soato=address_data['codeSoato'],
        street=address_data['street'],
        house=address_data['house'],
        flat=address_data['flat'],
        mail_index=address_data['mailIndex']
    )

@csrf_exempt
def signup(request: HttpRequest, *args, **kwargs):
    data = json.loads(request.body.decode())
    # pprint(data)
    user_data_fields = (
        'email', 'password', 'phoneNumber', 'salary',
        'name', 'surname', 'passportNumber', 'identificationNumber',
        'issueDate', 'expiryDate', 'authority', 'nationality',
        'sex', 'resident', 'birthDate',
        'registrationAddress', 'residentialAddress', 'birthAddress'
    )
    birth_address_fields = ('country', 'state', 'city')

    user_data = {}
    for data_field in user_data_fields:
        try:
            user_data[data_field] = data[data_field]
        except KeyError as err:
            return bad_request(f'{err} required')

    for field in birth_address_fields:
        if field not in user_data['birthAddress']:
            return bad_request(f'{field} in birth address is required')

    try:
        registration_address = parse_address(user_data['registrationAddress'])
        residential_address = parse_address(user_data['residentialAddress'])
    except KeyError as err:
        return bad_request(f'{err} in address is required')

    if User.objects.filter(email=user_data['email']).count() > 0:
        print(User.objects.filter(email=user_data['email']).count())
        return JsonResponse(
            data={
                "message": f"User with email '{user_data['email']}' already exists"
            },
            status=409
        )
    
    if len(user_data['password']) < 6:
        return bad_request('Password should be atleast 6 characters')

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(user_data['password'].encode(), salt)
    user = User(
        email=user_data['email'],
        password=hashed,
        salt=salt,
        phone_number=user_data['phoneNumber'],
        name=user_data['name'],
        surname=user_data['surname'],
        salary=user_data['salary']
    )
    user.save()
    # print('user saved')

    user_settings = UserSettings(
        user=user,
        preferred_currency=Currency.objects.get(name='BYN')
    )
    user_settings.save()
    # print('user settings saved')

    registration_address.save()
    residential_address.save()
    passport = PassportData(
        user=user,
        name=user_data['name'],
        surname=user_data['surname'],
        passport_number=user_data['passportNumber'],
        identification_number=user_data['identificationNumber'],
        issue_date=user_data['issueDate'],
        expiry_date=user_data['expiryDate'],
        authority=user_data['authority'],
        nationality=user_data['nationality'],
        sex=user_data['sex'],
        resident=user_data['resident'],
        birth_date=user_data['birthDate'],
        birth_country=user_data['birthAddress']['country'],
        birth_state=user_data['birthAddress']['state'],
        birth_city=user_data['birthAddress']['city'],
        registration_address=registration_address,
        residential_address=residential_address
    )
    passport.save()
    # print('passport saved')

    token = jwt.encode(
        {
            "id": user.pk
        }, 
        JWT_KEY, 
        algorithm='HS256'
    )
    log = Log(
        log = f'{user_data["email"]} registered'
    )
    log.save()
    return JsonResponse({
        "access_token": token
    })

class UserViewSet(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

class UserSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSettingsSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return UserSettings.objects.get(pk=self.request.user.pk)

    def get_queryset(self):
        return UserSettings.objects.filter(user=self.request.user)

class TelegramUsersViewSet(viewsets.ModelViewSet):
    serializer_class = TelegramUserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        if self.action == 'update':
            data = json.loads(self.request.body.decode())
            chat_id = int(data['chat_id'])
            tg_user = TelegramUser.objects.get(user=self.request.user, chat_id=chat_id)
            # print('tg_user', tg_user)
            return tg_user
        if self.action == 'destroy':
            data = self.request.GET
            chat_id = int(data['chat_id'])
            tg_user = TelegramUser.objects.get(user=self.request.user, chat_id=chat_id)
            return tg_user
        return super().get_object()


    def get_queryset(self):
        return TelegramUser.objects.filter(user=self.request.user)