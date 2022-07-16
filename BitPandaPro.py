#Importing the needed liberies
from typing import AsyncContextManager
import requests
import json
import re

from datetime import timedelta, datetime


#Declaring the API-version and the Bitpanda-API-URL's
BitpandaProURL = "https://api.exchange.bitpanda.com/public/v1"

#BitPandaPro Documentation "https://developers.bitpanda.com/exchange/#bitpanda-pro-api"
#URL to generate your Bitpanda-Pro API-Key: "https://exchange.bitpanda.com/account/keys"

class BitPandaPro(object):
  def __init__(self, api_key=None):
    self.api_key = api_key

  def market_time_to_datetime(market_time):
    m = re.match(r'(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)T(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)', market_time)
    return datetime(year=int(m['year']), month=int(m['month']), day=int(m['day']), hour=int(m['hour']), minute=int(m['minute']), second=int(m['second']))

  def set_api_key(self, api_key):
    self.api_key = api_key

  def get_api_key(self):
    return self.api_key

  def get_market_tickers(self, instrument_code=None):
    url = BitpandaProURL
    if instrument_code is None:
      url = url + '/market-ticker'
    else:
      url = url + '/market-ticker/' + instrument_code

    response = requests.get(url, headers = {'Accept': 'application/json'})

    data = response.json()
    if type(data) is not list:
      return [data]
    else:
      return data

  def get_candlestics(self, instrument_code, fr, to):
    url = BitpandaProURL
    url = url + '/candlesticks/' + instrument_code

    headers = {
      'Accept': 'application/json',
    }

    params = {}
    params.update({
      'unit': 'MINUTES',
      'period': '15',
      'from': fr.strftime('%Y-%m-%dT%H:%m:%SZ'),
      'to': to.strftime('%Y-%m-%dT%H:%m:%SZ')
    })

    response = requests.get(url, headers=headers, params=params)

    data = response.json()
    if type(data) is not list:
      return [data]
    else:
      return data

  def get_orders(self, instrument_code=None, with_cancelled_and_rejected=False, with_just_filled_inactive=False, with_just_orders=False):
    if self.api_key is None:
      return []

    url = BitpandaProURL + '/account/orders/'

    headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer {}'.format(self.api_key)
    }

    params = {}
    if instrument_code is not None:
      params.update({'instrument_code': instrument_code})

    if with_cancelled_and_rejected:
      params.update({'with_cancelled_and_rejected': True})

    if with_just_filled_inactive:
      params.update({'with_just_filled_inactive': True})

    if with_just_orders:
      params.update({'with_just_orders': True})

    response = requests.get(url, headers=headers, params=params)

    data = response.json()
    if type(data) is not list:
      return [data]
    else:
      return data

  def get_balances(self):
    if self.api_key is None:
      return []

    url = BitpandaProURL + '/account/balances/'

    headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer {}'.format(self.api_key)
    }

    params = {}

    response = requests.get(url, headers=headers, params=params)

    data = response.json()
    return data['balances']


  def create_limit_buy_order(self, instrument_code, amount, price):
    if self.api_key is None:
      return []

    url = BitpandaProURL + '/account/orders'

    order = {
      'instrument_code': instrument_code,
      'side': 'BUY',
      'type': 'LIMIT',
      'amount': str(amount),
      'price': str(price),
    }

    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Bearer {}'.format(self.api_key)
    }

    response = requests.post(url, headers=headers, data=json.dumps(order))

    return response.json()