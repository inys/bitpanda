#Importing the needed libraries
import requests
import json

#Declaring the API-version and the Bitpanda-API-URL's
BitPandaURL = "https://api.bitpanda.com/v1"

#BitPanda Documentation: "https://developers.bitpanda.com/platform/#bitpanda-public-api"
#URL to generate your Bitpanda API-Key: "https://web.bitpanda.com/apikey"

#The normal Bitpanda API is in this class
class BitPanda(object):

  def __init__(self, api_key):
    self.api_key = api_key

  def set_api_key(self, api_key):
    self.api_key = api_key

  def get_api_key(self):
    return self.api_key

  def get_trades(self):
    response = requests.get(BitPandaURL + '/trades', headers = {'X-API-KEY' : self.api_key}).json()

    try:
      data = response['data']
      output = []
      for i in range(len(data)):
        output.append({'type': data[i]['attributes']['type'], 'id': data[i]['id'], 'cryptocoin_id': data[i]['attributes']['cryptocoin_id'], 'amount_fiat': data[i]['attributes']['amount_fiat'], 'amount_cryptocoin': data[i]['attributes']['amount_cryptocoin'], 'crypto_price': data[i]['attributes']['price'], 'crypto_wallet_id': data[i]['attributes']['wallet_id'], 'date': data[i]['attributes']['time']['date_iso8601']})
      return output

    except:
      return response