from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
import jwt
from enum import Enum
import time
from hashlib import sha1
import requests
import json


from api.settings import JWT_KEY, WSB_STOREID, WEBPAY_SECRET_KEY
from ezaim.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()

        if len(auth_header) < 2:
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
wsb_notify_url = 'http://127.0.0.1:8000/notify/'

def pay_loan(
    wsb_order_num: str,
    wsb_test: int,
    wsb_currency: WebpayCurrency,
    wsb_total: str,
    wsb_customer_id: str,
    wsb_return_url: str
):
    wsb_seed = str(int(time.time()))
    signature = f'{wsb_seed}{WSB_STOREID}{wsb_customer_id}{wsb_order_num}{wsb_test}{wsb_currency.name}{wsb_total}{WEBPAY_SECRET_KEY}'
    wsb_signature = sha1(signature.encode()).hexdigest()

    body = {
        "wsb_language_id": "russian",
        "wsb_store": "EZAIM",
        # "wsb_tab": "cardPayment",
        # "wsb_card_halva": 0,
        "wsb_storeid": WSB_STOREID,
        "wsb_order_num": wsb_order_num,
        "wsb_currency_id": wsb_currency.name,
        "wsb_version": 2,
        "wsb_seed": wsb_seed,
        "wsb_test": wsb_test,
        "wsb_customer_id": wsb_customer_id,
        "wsb_signature": wsb_signature,
        "wsb_invoice_item_name": [
            'Ezaim. Оплата'
        ],
        "wsb_invoice_item_quantity": [
            1
        ],
        "wsb_invoice_item_price": [
            wsb_total
        ],
        "wsb_total": wsb_total,
        "wsb_return_url": wsb_return_url,
        "wsb_cancel_return_url": wsb_return_url,
        "wsb_notify_url": wsb_notify_url,
    }
    return body
    return requests.post(webpay_url, json=body)

def get_loan(
    wsb_order_num: str,
    wsb_test: int,
    wsb_currency: WebpayCurrency,
    wsb_total: str,
    wsb_token_p2p: str,
    wsb_customer_id: str
):
    wsb_seed = str(int(time.time()))

    signature = f'{wsb_seed}{WSB_STOREID}{wsb_order_num}{wsb_test}{wsb_currency.name}{wsb_total}{WEBPAY_SECRET_KEY}'
    wsb_signature = sha1(signature.encode()).hexdigest()

    body = {
        "wsb_language_id": "russian",
        "wsb_store": "EZAIM",
        # "wsb_tab": "cardPayment",
        # "wsb_card_halva": 0,
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
        "wsb_token_p2p": wsb_token_p2p,
        "wsb_output_via_corpocard_mtb": True,
        "wsb_customer_id": wsb_customer_id,        
    }
    return body
    return requests.post(webpay_url, json=body)

# def bind_card(
#     wsb_customer_id: str,
#     wsb_order_num: str,
#     wsb_test: int,
#     wsb_currency: WebpayCurrency,
#     wsb_total: str
# ):
#     wsb_seed = str(int(time.time()))
#     signature = f'{wsb_seed}{WSB_STOREID}{wsb_customer_id}{wsb_order_num}{wsb_test}{wsb_currency.name}{wsb_total}{WEBPAY_SECRET_KEY}'
#     wsb_signature = sha1(signature.encode()).hexdigest()

#     body = {
#         "wsb_customer_id": wsb_customer_id,
#         "wsb_operation_type": "recurring_bind",
#         "wsb_language_id": "russian",
#         "wsb_store": "EZAIM",
#         "wsb_storeid": WSB_STOREID,
#         "wsb_order_num": wsb_order_num,
#         "wsb_currency_id": wsb_currency.name,
#         "wsb_version": 2,
#         "wsb_seed": wsb_seed,
#         "wsb_test": wsb_test,
#         "wsb_signature": wsb_signature,
#         "wsb_invoice_item_name": [
#             'Ezaim. Оплата займа'
#         ],
#         "wsb_invoice_item_quantity": [
#             1
#         ],
#         "wsb_invoice_item_price": [
#             wsb_total
#         ],
#         "wsb_total": wsb_total,
#         "wsb_customer_id": wsb_customer_id
#     }
#     return body
