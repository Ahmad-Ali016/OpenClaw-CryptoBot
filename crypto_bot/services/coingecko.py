import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_crypto_prices():
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd,usdt"
    }

    response = requests.get(COINGECKO_URL, params=params)

    if response.status_code != 200:
        return None

    return response.json()


def format_prices(data):
    btc = data.get("bitcoin", {})
    eth = data.get("ethereum", {})

    btc_usd = btc.get("usd", "N/A")
    btc_usdt = btc.get("usdt", "N/A")

    eth_usd = eth.get("usd", "N/A")
    eth_usdt = eth.get("usdt", "N/A")

    message = f"""
 Crypto Prices

 BTC
 - USD: {btc_usd}
 - USDT: {btc_usdt}

 ETH
 - USD: {eth_usd}
 - USDT: {eth_usdt}
"""

    return message.strip()
