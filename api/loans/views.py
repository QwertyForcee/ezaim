from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

import json
from datetime import datetime, timedelta
from dateutil import relativedelta
from pprint import pprint
from decimal import Decimal
import pytz

from users.utils import JWTAuthentication
from loans.utils import pay_loan, get_loan, convert_currency
from loans.models import (
    Currency,
    Loan,
    PaymentCard,
    Payment,
    PercentOffer
)
from loans.serializers import *
from api.settings import MAX_ACTIVE_LOANS

def not_found(request, *args, **kwargs):
    return JsonResponse(data={"message": "Not Found"}, status=404)

def app_error(request, *args, **kwargs):
    return JsonResponse(data={"message": "Server Error"}, status=500)

def not_authorized(request, *args, **kwargs):
    return JsonResponse(data={"message": "Unauthorized"}, status=401)

def bad_request(request, message):
    return JsonResponse(data={"message": f'Bad Request: {message}'}, status=400)

class CurrencyViewSet(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def notify(request: HttpRequest, *args, **kwargs):
    data = request.GET
    print('notify response data')
    pprint(data)
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
    serializer_class = LoanSerializer

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)

    # def get_serializer_class(self):
    #     # if self.action == 'create':
    #     #     return NewLoanSerializer
    #     return LoanSerializer

    @action(detail=False, methods=["GET"], url_path="GetPercent", url_name="GetPercent")
    def getPercent(self, request: HttpRequest, *args, **kwargs):
        data = request.GET
        amount = Decimal(data['sum'])
        currency_id = int(data['currency'])
        try:
            currency = Currency.objects.get(pk=currency_id)
            percentOffers = PercentOffer.objects.filter(currency__pk=currency_id).order_by('amount')
            # print(percentOffers)
            if len(percentOffers) == 0:
                return not_found(request)
        except Exception:
            return not_found(request)
        percentOffer = None
        for offer in percentOffers:
            percentOffer = offer.percent
            if amount < offer.amount:
                break

        loans = Loan.objects.filter(user=self.request.user)
        monthly_pay = 0
        if currency.name == 'BYN':
            monthly_pay = amount * percentOffer
        else:
            monthly_pay = convert_currency(amount, currency.name, 'BYN') * percentOffer
        for loan in loans:
            if loan.currency.name != 'BYN':
                loan_amount = convert_currency(loan.amount, loan.currency.name, 'BYN')
            else:
                loan_amount = loan.amount
            monthly_pay += loan_amount * loan.percent
        salary = self.request.user.salary
        pdn = monthly_pay / salary
        print(f'monthly loans: {monthly_pay}, salary: {salary}, pdn: {pdn}')
        if pdn > 0.5:
            percentOffer *= 2

        print(f'{percentOffer*100:.1f}% for {amount}')
        return Response(percentOffer)

    @action(detail=False, methods=["POST"], url_path="GetCalculatedSumForLoan", url_name="GetCalculatedSumForLoan")
    def getCalculatedSum(self, request: HttpRequest, *args, **kwargs):
        data = json.loads(request.body.decode())
        loan_id = int(data['loanId']) # check name
        # print(f"request data: {data['date']}\n")
        estimate_date = datetime.fromisoformat(data['date'][:-1]+'+00:00') # check name, maybe needs localize
        estimate_date += timedelta(days=1, hours=2, minutes=59, seconds=59, microseconds=999999)
        # print(estimate_date)

        try:
            loan: Loan = Loan.objects.get(pk=loan_id)
        except ObjectDoesNotExist:
            return not_found(request)
        if not loan.is_active:
            return Response(0)
        utc = pytz.UTC
        # print(estimate_date, utc.localize(datetime.today()))
        if estimate_date < utc.localize(datetime.today()):
            return Response(0)
        delta = relativedelta.relativedelta(estimate_date, loan.created_at)
        estimated_months = delta.years * 12 + delta.months
        # print('estimated_months', estimated_months)
        # print('remaining', loan.remaining_amount)
        total_amount = (estimated_months + 1) * loan.percent * loan.amount - ((loan.months_passed + 1) * loan.percent * loan.amount - loan.remaining_amount)
        return Response(total_amount)


    def create(self, request, *args, **kwargs):
        data = json.loads(self.request.body.decode())
        print('loan create:')
        pprint(data)
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

        loans = Loan.objects.filter(user=self.request.user)

        active_loans_count = 0
        for loan in loans:
            if loan.is_active:
                active_loans_count += 1
        if active_loans_count >= MAX_ACTIVE_LOANS:
            return bad_request(request, 'Too many loans')

        monthly_pay = 0
        for loan in loans:
            if loan.currency.name != 'BYN':
                loan_amount = convert_currency(loan.amount, loan.currency.name, 'BYN')
            else:
                loan_amount = loan.amount
            monthly_pay += loan_amount * loan.percent
        salary = self.request.user.salary
        pdn = monthly_pay / salary
        print(f'monthly loans: {monthly_pay}, salary: {salary}, pdn: {pdn}')
        if pdn > 0.5:
            percentOffer *= 2

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
            print('bind card response')
            print(response)
            return Response(response['data']['redirectUrl'])
        payment_card = payment_cards[0]
        response = get_loan(
            f'loan-{new_loan.pk}',
            0,
            currency.name,
            str(amount),
            payment_card.token,
            f'customer-{self.request.user.pk}',
            return_url
        )
        print('get loan response')
        pprint(response)
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

    def create(self, request, *args, **kwargs):
        data = json.loads(self.request.body.decode())
        loan_id = int(data['loan'])
        amount = Decimal(data['amount'])
        return_url = data['return_url']
        # pprint(data)

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
        if loan.remaining_amount <= 0:
            loan.is_active = False
        loan.save()
        # pprint(response)
        return Response(response['data']['redirectUrl'])

class PaymentCardViewSet(viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin):
    # serializer_class = PaymentCardSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PaymentCard.objects.filter(owner_id=self.request.user)
