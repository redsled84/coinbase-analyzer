import os

API_PASS = os.environ.get("API_PASS")
API_SECRET = os.environ.get("API_SECRET")
API_KEY = os.environ.get("API_KEY")

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

api_url = 'https://api.pro.coinbase.com/'
auth = CoinbaseExchangeAuth(API_KEY, API_SECRET, API_PASS)

def get_account_info():
    global api_url, auth

    r = requests.get(api_url + 'accounts', auth=auth)
    accounts = r.json()
    total_value = 0

    info = {'data': [], 'total': 0}

    # iterate over every crypto wallet on my coinbase account
    for x in accounts:
        # ignore any cash or USDC on the account
        if str(x['currency']) == 'USD' or str(x['currency']) == 'USDC':
            continue
        # ignore any crypto that I'm not invested in
        elif float(x['balance']) > 0:
            prices_url = ""
            # DNT is my only coin that has a different ticker (USDC)
            if str(x['currency']) == "DNT":
                prices_url = api_url + 'products/DNT-USDC/ticker'
            else:
                prices_url = api_url + 'products/' + str(x['currency']) + '-USD/ticker'

            # process the request to get the coin price now that we have a proper API URL
            r = requests.get(prices_url, auth=auth)
            prices = r.json()
            value  = float(x['balance']) * float(prices['bid'])
            total_value += value

            # print('Balance', float(x['balance']), 'Currency', str(x['currency']), 'Total', value)
            info['data'].append({
                'balance': round(float(x['balance']), 7),
                'currency': str(x['currency']),
                'bid': round(float(prices['bid']), 5),
                'value': round(value, 2)
            })

    info['total'] = round(total_value, 2)
    info['data']  = sorted(info['data'], key = lambda i: (i['value']), reverse = True)

    return info

def get_crypto_data(symbol, days=220):
    response = requests.get("https://min-api.cryptocompare.com/data/v2/histoday?fsym=" + \
        symbol + "&tsym=USD&limit="+str(days)+"&api_key=431fcec5916d4ff75a52f7a615968306117c1b90591798fc513b023b79734fc2")
    return response.json()['Data']['Data']
