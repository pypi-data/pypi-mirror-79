# ClearSale API
---
ClearSale API setup and usage details.

## Dependencies
---
* Python 3.5

## How to setup
---
```
pip install git+ssh://git@gitlab.com/cotabest/clearsale.git
```

## API Reference
---
- https://api.clearsale.com.br/docs/home/how-to-start
- https://api.clearsale.com.br/docs/total-totalGarantido-application
- https://api.clearsale.com.br/docs/home/finger-print

## Usage
---
##### send_order

Create a new fraud analysis
```
import datetime

from clearsale.entities import (
	Order, Phone, Billing,
	Card, Payment, Item
)
from clearsale.api import ClearSale


phone = Phone(
	phone_type=Phone.CELULAR,
	ddd=11,
	number=983485056
)

billing = Billing(
	customer_type=Billing.TYPE_PESSOA_FISICA,
	primaryDocument='12345678910',
	name='Complete Client Name',
	email='hugosunno@gmail.com'
)

billing.phones.append(phone)

card = Card(
	six_first_digits='123456',
	four_last_digits='0987',
	ownerName='Fulano De Tal',
	validityDate='02/2021',
	document='12345678910',
)

payment = Payment(
	payment_type=Payment.CARTAO_CREDITO,
	card=card
)

item1 = Item(
	code='00001',
	name='Item 1 description',
	value=float(9.99),
	amount=5,
	sellerName='Company A',
	sellerDocument='00000000001'
)

item2 = Item(
	code='00002',
	name='Item 2 description',
	value=float(13.09),
	amount=2,
	sellerName='Company B',
	sellerDocument='00000000002'

)

order = Order(
	code='123',
	sessionID='1234567',
	email='hugosunno@gmail.com',
	totalValue=float(200.50),
	billing=billing
)

order.payments.append(payment)
order.items.append(item1)
order.items.append(item2)

instance = ClearSale(sandbox=True)
username = 'Cotabest_TG'
password = 'b83feGKtpg'

auth = instance.authenticate(username, password)
token = auth.get('Token')

response = instance.send_order(order, token)

In [6]: response.json()
Out[6]: {'packageID': 'c503dcb1-25e9-48a1-bcb4-4a89d0c5732f',
 'orders': [{'code': '123', 'status': 'NVO', 'score': None}]}
```

---

##### get_order

Get a fraud analysis details
```
from clearsale.api import ClearSale

instance = ClearSale(sandbox=True)
username = 'Cotabest_TG'
password = 'b83feGKtpg'
order_id = '1234'

auth = instance.authenticate(username, password)
token = auth.get('Token')

response = instance.get_order(order_id, token)

In [6]: response.json()
Out[6]: {'code': '1234', 'status': 'AMA', 'score': 98.98}
```
