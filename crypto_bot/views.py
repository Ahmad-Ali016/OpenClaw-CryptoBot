import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services.coingecko import get_crypto_prices, format_prices
from .services.parser import parse_command


# Create your views here.

@csrf_exempt
def webhook(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"})

    data = json.loads(request.body)

    message = data.get("message", "").lower()

    print("Incoming message:", message)

    command = parse_command(message)

    if not command:
        return JsonResponse({
            "reply": "Unknown command. Try: price, btc, eth"
        })

    prices = get_crypto_prices()

    if not prices:
        return JsonResponse({
            "reply": "Error fetching crypto prices"
        })

    reply = format_prices(prices, command["coins"])

    return JsonResponse({
        "reply": reply
    })


# @csrf_exempt
# def webhook(request):
#
#     if request.method == "POST":
#
#         data = json.loads(request.body)
#
#         message = data.get("message", "").lower()
#
#         return JsonResponse({
#             "reply": f"Received command: {message}"
#         })
#
#     return JsonResponse({"error": "Invalid request"})