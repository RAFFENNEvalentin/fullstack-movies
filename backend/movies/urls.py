from django.urls import path
from django.http import JsonResponse
from .views import health, health_async

async def api_root(request):
    return JsonResponse({"status": "api ready"})

urlpatterns = [
    path("", api_root, name="api-root"),
    path("health/", health, name="health"),              
    path("health_async/", health_async, name="health-async"),  
]