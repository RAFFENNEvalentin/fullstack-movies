# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HealthSerializer
from django.http import JsonResponse

# DRF best practice: Response + Serializer
@api_view(["GET"])
def health(request):
    payload = {"status": "ok"}
    serializer = HealthSerializer(payload)
    return Response(serializer.data)


async def health_async(request):
    return JsonResponse({"status": "ok"})