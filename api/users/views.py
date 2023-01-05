from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

import jwt
import json
import bcrypt

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

def not_found(request, *args, **kwargs):
    return JsonResponse(data={"message": "Not Found"}, status=404)

def app_error(request, *args, **kwargs):
    return JsonResponse(data={"message": "Server Error"}, status=500)

def not_authorized(request, *args, **kwargs):
    return JsonResponse(data={"message": "Unauthorized"}, status=401)

def bad_request(request, message):
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
    log = Log(
        log=f'{email} logged in'
    )
    log.save()
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
    # pprint(data)

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

    try:
        # birth_address = parse_address(data['birthAddress'])
        registration_address = parse_address(data['registrationAddress'])
        registration_address.save()
        # print('reg add saved')
        residential_address = parse_address(data['residentialAddress'])
        residential_address.save()
        # print('res add saved')
    except Exception:
        print('something went wrong')


    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    user = User(
        email=email,
        password=hashed,
        salt=salt,
        phone_number=phone_number,
        name=name,
        surname=surname,
        salary=salary
    )
    user.save()
    # print('user saved')
    user_settings = UserSettings(
        user=user,
        preferred_currency=Currency.objects.get(name='BYN')
    )
    user_settings.save()
    # print('user settings saved')

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
    # print('passport saved')

    token = jwt.encode(
        {
            "id": user.pk
        }, 
        JWT_KEY, 
        algorithm='HS256'
    )
    log = Log(
        log = f'{email} registered'
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
    # queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_queryset(self):
        # print('getting objects')
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