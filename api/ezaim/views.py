from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets, mixins

from ezaim.models import (
    User, TelegramUser, UserSettings,
    PaymentCard, Payment, Loan, 
    Currency, Log
)
from ezaim.serializers import (
    UserSerializer,
    UserSettingsSerializer,
    CurrencySerializer,
    LoanSerializer,
    PaymentSerializer,
    PaymentCardSerializer
)


def not_found(request, *args, **kwargs):
    return JsonResponse(data={"message": "Not Found"}, status=404)

def app_error(request, *args, **kwargs):
    return JsonResponse(data={"message": "Server Error"}, status=500)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer

    # def update(self, request, pk=None, *args, **kwargs):
    #     instance = self.get_object()
    #     print(request)


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentCardViewSet(viewsets.ModelViewSet):
    queryset = PaymentCard.objects.all()
    serializer_class = PaymentCardSerializer