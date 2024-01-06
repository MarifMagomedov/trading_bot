import requests


def get_crypto_prices():
    url = 'https://api.coinlore.net/api/tickers/?start=0&limit=10'
    result = requests.get(url).json()
    text = []
    for data in sorted(result['data'], key=lambda x: float(x['price_usd']), reverse=True):
        crypto = data['symbol']
        price = round(float(data['price_usd']), 2)
        text.append([f"{crypto} {price} $", f'crypto:{crypto}:{price}'])
    return text


def get_crypto_price(crypto):
    url = 'https://api.coinlore.net/api/ticker/?id='
    currencies_id = {
        'BTC': '90',
        'ETH': '80',
        'USDT': '518',
        'BNB': '2710',
        'SOL': '48543',
        'XRP': '58',
        'USDC': '33285',
        'STETH': '46971',
        'ADA': '257',
        'AVAX': '44883'
    }
    price = float(requests.get(url + currencies_id[crypto]).json()[0]['price_usd'])
    return price
