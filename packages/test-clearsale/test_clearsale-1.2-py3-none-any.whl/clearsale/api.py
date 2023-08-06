import json
from datetime import datetime
from unicodedata import normalize
from collections import OrderedDict

import requests


class ClearSale():

    URL_PRODUCTION = 'https://api.clearsale.com.br/v1/'
    URL_HOMOLOGATION = 'https://homologacao.clearsale.com.br/api/v1/'

    def __init__(self, fingerprint=None, sandbox=False):
        self.url = self.URL_HOMOLOGATION if sandbox else self.URL_PRODUCTION
        self.fingerprint = fingerprint

    def authenticate(self, username, password):
        url = self.url + 'authenticate'
        data = {'name': username, 'password': password}
        authentication = requests.post(url=url, data=data)

        if not authentication.ok:
            raise Exception(f'Authentication failed: {authentication.text}')

        return authentication.json()

    def send_order(self, order, auth_token):
        data = {
            'code': order.code,
            'sessionID': order.sessionID,
            'date': datetime.now().isoformat(),
            'email': order.email,
            'totalValue': order.totalValue,
            'numberOfInstallments': order.numberOfInstallments,
            'ip': order.ip,
            'status': order.status,
            'billing': {
                'type': order.billing.customer_type,
                'primaryDocument': order.billing.primaryDocument,
                'name': order.billing.name,
                'email': order.billing.email,
                'phones': [{
                        'type': i.phone_type,
                        'ddd': i.ddd,
                        'number': i.number,
                    } for i in order.billing.phones
                ]
            },
            'payments': [{
                    'type': i.payment_type,
                    'installments': i.installments,
                    'currency': 986, #BRL
                    'card': {
                        'number': i.card.number,
                        'bin': i.card.six_first_digits,
                        'end': i.card.four_last_digits,
                        'ownerName': i.card.ownerName,
                        'validityDate': i.card.validityDate,
                        'document': i.card.document,
                    },
                } for i in order.payments
            ],
            'items': [{
                    'code': i.code,
                    'name': i.name,
                    'value': i.value,
                    'amount': i.amount,
                    'sellerName': i.sellerName,
                    'sellerDocument': i.sellerDocument,
                } for i in order.items
            ]
        }

        url = self.url + 'orders'
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.post(url=url, data=json.dumps(data), headers=headers)

        if not response.ok:
            raise Exception(f'Order not sent: {response.text}')

        return response

    def get_order(self, order_id, auth_token):
        url = self.url + f'orders/{order_id}/status'
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Accept': 'application/json'
        }
        response = requests.get(url=url, headers=headers)

        if not response.ok:
            raise Exception(f'Order not found: {response.text}')

        return response
