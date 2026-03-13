import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services.coingecko import get_crypto_prices, format_prices

# Create your views here.

@csrf_exempt
def webhook(request):

    if request.method == "POST":

        data = json.loads(request.body)

        message = data.get("message", "").lower()

        # handle price command
        if message == "price":

            prices = get_crypto_prices()

            if not prices:
                return JsonResponse({"reply": "Error fetching prices"})

            reply = format_prices(prices)

            return JsonResponse({"reply": reply})

        # unknown command
        return JsonResponse({
            "reply": "Unknown command. Try: price"
        })

    return JsonResponse({"error": "Invalid request"})


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