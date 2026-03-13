def parse_command(message):

    message = message.lower().strip()

    if message == "price":
        return {
            "coins": ["bitcoin", "ethereum"],
            "currency": None
        }

    if message == "btc":
        return {
            "coins": ["bitcoin"],
            "currency": None
        }

    if message == "eth":
        return {
            "coins": ["ethereum"],
            "currency": None
        }

    return None