import requests
import logging

logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


def get_crypto_prices(coins):
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd,usdt,pkr"
    }

    try:
        response = requests.get(
            COINGECKO_URL,
            params=params,
            timeout=10,
            headers={"User-Agent": "OpenClaw-CryptoBot"}
        )

        # print("CoinGecko Status:", response.status_code)
        logger.info("CoinGecko status: %s", response.status_code)

        if response.status_code != 200:
            # print("CoinGecko Response:", response.text)
            logger.warning("CoinGecko response: %s", response.text)
            return None

        data = response.json()
        # print("CoinGecko Data:", data)

        logger.debug("CoinGecko data: %s", data)

        return data

    except Exception as e:
        # print("CoinGecko Error:", str(e))
        logger.error("CoinGecko error: %s", str(e))
        return None



def format_prices(data, coins=None):

    if coins is None:
        coins = ["bitcoin", "ethereum"]

    coin_labels = {
        "bitcoin": "BTC",
        "ethereum": "ETH"
    }

    message = "Crypto Prices\n\n"

    usd_pkr_ratio = None

    for coin in coins:

        coin_data = data.get(coin, {})

        usd = coin_data.get("usd", "N/A")
        usdt = coin_data.get("usdt", "N/A")
        pkr = coin_data.get("pkr", "N/A")

        label = coin_labels.get(coin, coin.upper())

        message += f"""{label}
 > USD: {usd}
 > USDT: {usdt}
 > PKR: {pkr}

"""

        # calculate ratio if possible
        if usd != "N/A" and pkr != "N/A" and usd_pkr_ratio is None:
            try:
                usd_pkr_ratio = round(float(pkr) / float(usd), 2)
            except Exception:
                pass

    if usd_pkr_ratio:
        message += f"""USD ↔ PKR Ratio
 > 1 USD ≈ {usd_pkr_ratio} PKR
"""

    return message.strip()