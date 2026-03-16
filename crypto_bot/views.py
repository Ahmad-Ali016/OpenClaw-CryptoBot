import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

from .services.coingecko import get_crypto_prices, format_prices
from .services.parser import parse_command

# Create your views here.

logger = logging.getLogger(__name__)

def health(request):
    return JsonResponse({"status": "ok"})

@csrf_exempt
def webhook(request):
    # Validate HTTP method
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests allowed"},
            status=405
        )

    # Validate body exists
    if not request.body:
        return JsonResponse(
            {"error": "Empty request body"},
            status=400
        )

    # Validate JSON format
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400
        )

    # Extract message from multiple payload formats
    message = (
            data.get("message")
            or data.get("text")
            or data.get("body")
    )

    # Handle nested formats like { "message": { "text": "price" } }
    if isinstance(message, dict):
        message = message.get("text")

    if not message:
        return JsonResponse(
            {"error": "Missing 'message' field"},
            status=400
        )

    message = message.lower().strip()
    logger.info("Incoming message: %s", message)

    # Parse command
    command = parse_command(message)

    if not command:
        return JsonResponse({
            "reply": "Unknown command. Try: price, btc, eth"
        })

    # Fetch crypto prices
    prices = get_crypto_prices()

    if not prices:
        logger.warning("Failed to fetch crypto prices")
        return JsonResponse({
            "reply": "Error fetching crypto prices"
        })

    # Format response
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
