from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt
from enum import Enum
import time
from hashlib import sha1
import requests
import json
import rsa

from api.settings import JWT_KEY, WSB_STOREID, WEBPAY_SECRET_KEY
from ezaim.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()

        if len(auth_header) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth_header[1]
            id = jwt.decode(token, JWT_KEY, algorithms=['HS256']).get('id', None)
            if id is None:
                raise User.DoesNotExist
            user = User.objects.get(pk=id)
            
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, token)

class WebpayCurrency(Enum):
    BYN = 'BYN'
    RUB = 'RUB'
    EUR = 'EUR'
    USD = 'USD'



webpay_url = 'https://securesandbox.webpay.by/api/v1/payment'

def pay_loan(
    wsb_order_num: str,
    wsb_test: int,
    wsb_currency: WebpayCurrency,
    wsb_total: str
):
    wsb_seed = str(int(time.time()))
    signature = f'{wsb_seed}{WSB_STOREID}{wsb_order_num}{wsb_test}{wsb_currency.name}{wsb_total}{WEBPAY_SECRET_KEY}'
    wsb_signature = sha1(signature.encode()).hexdigest()

    body = {
        "wsb_storeid": WSB_STOREID,
        "wsb_order_num": wsb_order_num,
        "wsb_currency_id": wsb_currency.name,
        "wsb_version": 2,
        "wsb_seed": wsb_seed,
        "wsb_test": wsb_test,
        "wsb_signature": wsb_signature,
        "wsb_invoice_item_name": [
            'Ezaim. Оплата займа'
        ],
        "wsb_invoice_item_quantity": [
            1
        ],
        "wsb_invoice_item_price": [
            wsb_total
        ],
        "wsb_total": wsb_total
    }
    return body
    return requests.post(webpay_url, json=body)

def get_loan(
    wsb_order_num: str,
    wsb_test: int,
    wsb_currency: WebpayCurrency,
    wsb_total: str,
    card_pan: str,
    card_exp: str,
    card_cvv: str,
    card_name: str
):
    wsb_seed = str(int(time.time()))

    card_info = {
        "cc_pan": card_pan,
        "cc_exp": card_exp,
        "cc_cvv": card_cvv,
        "cc_name": card_name
    }
    rsa_key = rsa.PublicKey.load_pkcs1(WEBPAY_SECRET_KEY.encode())
    wsb_encrypted_data = rsa.encrypt(
        json.dumps(card_info).encode(), 
        rsa_key
    ).hex()
    signature = f'{wsb_seed}{WSB_STOREID}{wsb_order_num}{wsb_test}{wsb_currency.name}{wsb_total}{wsb_encrypted_data}{WEBPAY_SECRET_KEY}'
    wsb_signature = sha1(signature.encode()).hexdigest()

    body = {
        "wsb_storeid": WSB_STOREID,
        "wsb_order_num": wsb_order_num,
        "wsb_currency_id": wsb_currency.name,
        "wsb_version": 2,
        "wsb_seed": wsb_seed,
        "wsb_test": wsb_test, # for testing needs to be 0 if money draw?
        "wsb_signature": wsb_signature,
        "wsb_invoice_item_name": [
            'Ezaim. Получение займа'
        ],
        "wsb_invoice_item_quantity": [
            1
        ],
        "wsb_invoice_item_price": [
            wsb_total
        ],
        "wsb_total": wsb_total,
        "wsb_encrypted_data": wsb_encrypted_data,
        "wsb_output_via_corpocard": True
    }
    return body
    return requests.post(webpay_url, json=body)
