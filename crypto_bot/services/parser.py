COIN_MAP = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "xrp": "ripple",
        "doge": "dogecoin",
    }

def parse_command(message):

    parts = message.split()

    # example: "price btc"
    if len(parts) == 2 and parts[0] == "price":
        coin = COIN_MAP.get(parts[1])
        if coin:
            return {"coins": [coin]}

    # example: "btc"
    if message in COIN_MAP:
        return {"coins": [COIN_MAP[message]]}

    # example: "price"
    if message == "price":
        return {"coins": ["bitcoin", "ethereum"]}

    return None