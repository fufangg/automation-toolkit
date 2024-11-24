import requests


def get_crypto_price(crypto):
    url = f"https://api.coindesk.com/v1/bpi/currentprice/{crypto}.json"
    response = requests.get(url)
    data = response.json()
    return data['bpi']['USD']['rate']


print(get_crypto_price('BTC'))