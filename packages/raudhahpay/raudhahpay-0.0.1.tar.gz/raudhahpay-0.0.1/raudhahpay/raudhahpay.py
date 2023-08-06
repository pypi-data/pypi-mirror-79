import datetime

import requests


class RaudhahPay:

    def __init__(self, config: dict):
        self.signature_key = config.get('signature_key')
        self.api_key = config.get('api_key')
        self.base_url = config.get('base_url')

        self.collection_code = None
        self.f_name = None
        self.l_name = None
        self.email = None
        self.phone = None
        self.address = None
        self.ref = None

        self.product_name = None
        self.product_price: float = 0
        self.quantity: int = 0

    def make_bill(self, collection_code: str):
        self.collection_code = collection_code
        return self

    def make_cust(self, f_name, l_name, email, phone, address):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.phone = phone
        self.address = address
        return self

    def make_ref(self, ref):
        self.ref = ref
        return self

    def make_product(self, name, price: float, quantity: int):
        self.product_name = name
        self.product_price = price
        self.quantity = quantity
        return self

    def generate(self):
        url = self.base_url + '/collections/' + self.collection_code + '/bills'

        data = {
            'due': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            'currency': 'MYR',
            'ref1': self.ref,
            'ref2': self.ref,
            'customer': {
                'first_name': self.f_name,
                'last_name': self.l_name,
                'address': self.address,
                'email': self.email,
                'mobile': self.phone
            },
            'product': [
                {
                    'title': self.product_name,
                    'price': self.product_price,
                    'quantity': self.quantity
                }
            ]
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key
        }

        req = requests.post(url, json=data, headers=headers)
        return req
