from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import viewsets, mixins
import jwt

from django.views.decorators.csrf import csrf_exempt


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

def not_authorized(request, *args, **kwargs):
    return JsonResponse(data={"message": "Unauthorized"}, status=401)

# todo: get key from settings from dotenv
# todo: return csrf cookies
key = 'roflan'
@csrf_exempt
def login(request, *args, **kwargs):
    email, password = request.POST['email'], request.POST['password']
    try:
        user = User.objects.get(email=email)
        if user.password != password:
            return not_authorized(request)
    except ObjectDoesNotExist:
        return not_found(request)
    except MultipleObjectsReturned:
        return app_error(request)
    token = jwt.encode(
        {
            "id": user.pk
        }, 
        key, 
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