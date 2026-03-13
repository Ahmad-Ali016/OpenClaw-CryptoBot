import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_crypto_prices():
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd,pkr"
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
    btc_pkr = btc.get("pkr", "N/A")

    eth_usd = eth.get("usd", "N/A")
    eth_usdt = eth.get("usdt", "N/A")
    eth_pkr = eth.get("pkr", "N/A")

    # Calculate ETH <-> PKR relation (if both values exist)
    usd_pkr_ratio = "N/A"
    if eth_usd != "N/A" and eth_pkr != "N/A":
        try:
            usd_pkr_ratio = round(float(eth_pkr) / float(eth_usd), 2)
        except Exception:
            usd_pkr_ratio = "N/A"

    message = f"""
 Crypto Prices

 BTC
 > USD: {btc_usd}
 > USDT: {btc_usdt}
 > PKR: {btc_pkr}

 ETH
 > USD: {eth_usd}
 > USDT: {eth_usdt}
 > PKR: {eth_pkr}
 
 USD ↔ PKR Ratio
 > 1 USD ≈ {usd_pkr_ratio} PKR
"""

    return message.strip()
