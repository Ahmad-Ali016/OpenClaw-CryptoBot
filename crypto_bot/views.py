import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@csrf_exempt
def webhook(request):

    if request.method == "POST":

        data = json.loads(request.body)

        message = data.get("message", "").lower()

        return JsonResponse({
            "reply": f"Received command: {message}"
        })

    return JsonResponse({"error": "Invalid request"})