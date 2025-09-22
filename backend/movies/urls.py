from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from .views import health, health_async, MovieViewSet

async def api_root(request):
    return JsonResponse({"status": "api ready"})

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")

urlpatterns = [
    path("", api_root, name="api-root"),
    path("health/", health, name="health"),
    path("health_async/", health_async, name="health-async"),
    path("", include(router.urls)),
]