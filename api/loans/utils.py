import time
from hashlib import sha1
import requests
import json
from pprint import pprint
from decimal import Decimal

from api.settings import WSB_STOREID, WEBPAY_SECRET_KEY, EXCHANGE_RATE_API_KEY


def convert_currency(amount, currency_from, currency_to):
    print(f'converting {amount}{currency_from} to {currency_to}')
    # temp
    if currency_from == 'USD' and currency_to == 'BYN':
        return amount * Decimal('2.5')
    
    response = requests.get(
        "https://api.apilayer.com/exchangerates_data/convert", 
        params = {
            'amount': amount,
            'from': currency_from,
            'to': currency_to
        },
        headers = {
            'apikey': EXCHANGE_RATE_API_KEY
        }
    )
    pprint(response.json())
    return Decimal(f"{response.json()['result']:.4f}")


webpay_url = 'https://securesandbox.webpay.by/api/v1/payment'
wsb_notify_url = 'http://127.0.0.1:8000/notify/'
currencies = ('BYN', 'USD')

def pay_loan(
    wsb_order_num: str,
    wsb_test: int,
    wsb_currency: str,
    wsb_total: str,
    wsb_customer_id: str,
    wsb_return_url: str
):
    if wsb_currency not in currencies:
        return None
    wsb_seed = str(int(time.time()))
    signature = f'{wsb_seed}{WSB_STOREID}{wsb_customer_id}{wsb_order_num}{wsb_test}{wsb_currency}{wsb_total}{WEBPAY_SECRET_KEY}'
    wsb_signature = sha1(signature.encode()).hexdigest()

    body = {
        "wsb_language_id": "russian",
        # "wsb_store": "EZAIM",
        # "wsb_tab": "cardPayment",
        # "wsb_card_halva": 0,
        "wsb_storeid": WSB_STOREID,
        "wsb_order_num": wsb_order_num,
        "wsb_currency_id": wsb_currency,
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
        # "wsb_notify_url": wsb_notify_url,
    }
    print('pay loan body:')
    pprint(body)
    
    # return body
    return requests.post(webpay_url, json=body).json()

def get_loan(
    wsb_order_num: str,
    wsb_test: int,
    wsb_currency: str,
    wsb_total: str,
    wsb_token_p2p: str,
    wsb_customer_id: str,
    wsb_return_url: str
):
    if wsb_currency not in currencies:
        return None
    
    wsb_seed = str(int(time.time()))
    signature = f'{wsb_seed}{WSB_STOREID}{wsb_customer_id}{wsb_order_num}{wsb_test}{wsb_currency}{wsb_total}{WEBPAY_SECRET_KEY}'
    wsb_signature = sha1(signature.encode()).hexdigest()

    body = {
        # "wsb_language_id": "russian",
        # "wsb_store": "EZAIM",
        # "wsb_tab": "cardPayment",
        # "wsb_card_halva": 0,
        "wsb_storeid": WSB_STOREID,
        "wsb_order_num": wsb_order_num,
        "wsb_currency_id": wsb_currency,
        "wsb_version": 2,
        "wsb_seed": wsb_seed,
        "wsb_test": wsb_test, # for testing needs to be 0 if money draw?
        "wsb_signature": wsb_signature,
        # "wsb_invoice_item_name": [
        #     'Ezaim. Получение займа'
        # ],
        # "wsb_invoice_item_quantity": [
        #     1
        # ],
        # "wsb_invoice_item_price": [
        #     wsb_total
        # ],
        "wsb_total": wsb_total,
        "wsb_token_p2p": wsb_token_p2p,
        "wsb_output_via_corpocard_mtb": True,
        "wsb_customer_id": wsb_customer_id, 
        "wsb_return_url": wsb_return_url,       
    }
    print('get loan body:')
    pprint(body)
    # return body
    return requests.post('https://securesandbox.webpay.by/output/mtb', json=body).json()
