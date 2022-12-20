from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import jwt
import json
import bcrypt
from datetime import datetime
from dateutil import relativedelta
#
import pprint
from decimal import *

from api.settings import JWT_KEY
from ezaim.utils import JWTAuthentication
from ezaim.utils import pay_loan, get_loan
from django.views.decorators.csrf import csrf_exempt

from ezaim.models import *
from ezaim.serializers import *


def not_found(request, *args, **kwargs):
    return JsonResponse(data={"message": "Not Found"}, status=404)

def app_error(request, *args, **kwargs):
    return JsonResponse(data={"message": "Server Error"}, status=500)

def not_authorized(request, *args, **kwargs):
    return JsonResponse(data={"message": "Unauthorized"}, status=401)


@csrf_exempt
def login(request: HttpRequest, *args, **kwargs):
    data = json.loads(request.body.decode())
    email, password = data['email'], data['password']

    try:
        user = User.objects.get(email=email)
        hashed = bcrypt.hashpw(password.encode(), user.salt)
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

    # pprint.pprint(data)

    email = data.get('email', None)
    password = data.get('password', None)
    phone_number = data.get('phoneNumber', None)
    password = data.get('password', None)

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
        name=name,
        surname=surname
    )
    user.save()
    print('user saved')
    user_settings = UserSettings(
        user=user,
        currency=Currency.objects.get(name='BYN')
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
        mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

class CurrencyViewSet(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

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
            print('tg_user', tg_user)
            return tg_user
        if self.action == 'destroy':
            data = self.request.GET
            chat_id = int(data['chat_id'])
            tg_user = TelegramUser.objects.get(user=self.request.user, chat_id=chat_id)
            return tg_user
        return super().get_object()


    def get_queryset(self):
        return TelegramUser.objects.filter(user=self.request.user)

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def notify(request: HttpRequest, *args, **kwargs):
    data = request.GET
    pprint.pprint(data)
    order_num = data['wsb_order_num']
    loan_id = int(order_num)
    token = data.get('wsb_tid', None)
    loans_link = 'http://localhost:4200/loans'
    if token is None:
        print('transaction was cancelled, need to delete loan')
        try:
            loan = Loan.objects.get(pk=loan_id)
            loan.delete()
        except ObjectDoesNotExist:
            print(f'loan#{loan_id} not found; token not found')
    else:
        print('got token, need to bind payment card' )
        try:
            loan: Loan = Loan.objects.get(pk=loan_id)
        except ObjectDoesNotExist:
            print(f'loan#{loan_id} not found; token not found')
        print('user', loan.user)
        new_payment_card = PaymentCard(
            token = token,
            user = loan.user,
        )
        new_payment_card.save()
    return HttpResponseRedirect(loans_link)


class LoanViewSet(
        viewsets.GenericViewSet, 
        mixins.ListModelMixin, 
        mixins.CreateModelMixin, 
        mixins.RetrieveModelMixin):  
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        # if self.action == 'create':
        #     return NewLoanSerializer
        return LoanSerializer

    @action(detail=False, methods=["POST"], url_path="GetPercent", url_name="GetPercent")
    def getPercent(self, request: HttpRequest, *args, **kwargs):
        data = request.GET
        amount = Decimal(data['sum'])
        currency_id = int(data['currency'])
        try:
            percentOffers = PercentOffer.objects.filter(currency__pk=currency_id).order_by('amount')
            print(percentOffers)
            if len(percentOffers) == 0:
                return not_found(request)
        except Exception:
            return not_found(request)
        percentOffer = None
        for offer in percentOffers:
            percentOffer = offer.percent
            if amount < offer.amount:
                break
        print(f'{percentOffer*100:.1f}% for {amount}')
        return Response(percentOffer)

    @action(detail=False, methods=["POST"], url_path="GetCalculatedSumForLoan", url_name="GetCalculatedSumForLoan")
    def getCalculatedSum(self, request: HttpRequest, *args, **kwargs):
        data = json.loads(request.body.decode())
        loan_id = int(data['loanId']) # check name
        estimate_date = datetime(data['date']) # check name, maybe needs localize
        try:
            loan: Loan = Loan.objects.get(pk=loan_id)
        except ObjectDoesNotExist:
            return not_found(request)
        delta = relativedelta.relativedelta(estimate_date, loan.created_at)
        estimated_months = delta.years * 12 + delta.months
        total_amount = estimated_months * loan.percent * loan.amount - loan.remaining_amount
        return Response(total_amount)


    def create(self, request, *args, **kwargs):
        print('loan create')
        data = json.loads(self.request.body.decode())
        currency_id = int(data['currency'])
        amount = Decimal(data['amount'])
        return_url = data['return_url']

        try:
            currency = Currency.objects.get(pk=currency_id)
            percentOffers = PercentOffer.objects.filter(currency=currency).order_by('amount')
            if len(percentOffers) == 0:
                return not_found(self.request)
        except Exception:
            return not_found(self.request)
        percentOffer = None
        for offer in percentOffers:
            percentOffer = offer.percent
            if amount < offer.amount:
                break
        
        remaining_amount = amount * (percentOffer + 1)
        new_loan = Loan(
            user = self.request.user,
            percent = percentOffer,
            amount = amount,
            remaining_amount = remaining_amount,
            currency = currency
        )
        new_loan.save()

        payment_cards = PaymentCard.objects.filter(user=self.request.user)
        if len(payment_cards) == 0:
            # needs binding
            response = pay_loan(
                f'{new_loan.pk}',
                1,
                currency.name,
                1,
                f'customer-{self.request.user.id}',
                'http://127.0.0.1:8000/notify/'
            )
            print(response)
            return Response(response['data']['redirectUrl'])
        payment_card = payment_cards[0]
        get_loan(
            f'loan-{new_loan.pk}',
            0,
            currency.name,
            str(amount),
            payment_card.token,
            f'customer-{self.request.user.pk}',
            return_url
        )
        return Response(return_url)


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

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return PaymentSerializer
    #     return PaymentCardSerializer

    def create(self, request, *args, **kwargs):
        data = json.loads(self.request.body.decode())
        loan_id = int(data['loan'])
        amount = Decimal(data['amount'])
        return_url = data['return_url']

        try:
            loan = Loan.objects.get(pk=loan_id)
        except Exception:
            return not_found(self.request)
        
        new_payment = Payment(
            amount=amount,
            loan=loan
        )
        new_payment.save()
        
        response = pay_loan(
            f'payment-{new_payment.pk}',
            0,
            loan.currency.name,
            str(amount),
            f'customer-{self.request.user.pk}',
            return_url
        )
        if response is None:
            return not_found()
        loan.remaining_amount = loan.remaining_amount - amount
        loan.save()
        return Response(response['data']['redirectUrl'])

class PaymentCardViewSet(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin):
    # serializer_class = PaymentCardSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PaymentCard.objects.filter(owner_id=self.request.user)
