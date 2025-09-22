# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.db.models import Avg, Prefetch

from .serializers import HealthSerializer, MovieSerializer, ReviewSerializer, ActorSerializer
from .models import Movie, Actor, Review


@api_view(["GET"])
def health(request):
    payload = {"status": "ok"}
    serializer = HealthSerializer(payload)
    return Response(serializer.data)


async def health_async(request):
    return JsonResponse({"status": "ok"})

# ---- Movie API (DRF) ----
class MovieViewSet(viewsets.ModelViewSet):
    """
    list:    GET /api/movies/         (paginé par DRF: 5 items/page)
    retrieve:GET /api/movies/{id}/    (inclut actors + average_grade)
    partial_update: PATCH /api/movies/{id}/  (description, actor_ids)
    create/update/delete: non utilisés pour l’instant
    POST /api/movies/{id}/reviews/    -> ajoute une review (grade 1..5)
    """
    serializer_class = MovieSerializer

    def get_queryset(self):
        # Optimisations: prefetch acteurs + annotate moyenne en DB
        return (
            Movie.objects.all()
            .prefetch_related(
                Prefetch("actors", queryset=Actor.objects.only("id", "first_name", "last_name"))
            )
            .annotate(average_grade=Avg("reviews__grade"))
            .order_by("-id")
        )

    @action(detail=True, methods=["post"], url_path="reviews")
    def add_review(self, request, pk=None):
        """POST /api/movies/{id}/reviews/  body: {"grade": int}"""
        movie = self.get_object()
        ser = ReviewSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        Review.objects.create(movie=movie, grade=ser.validated_data["grade"])
        return Response({"status": "created"}, status=status.HTTP_201_CREATED)
    

class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Actor.objects.all().order_by("last_name", "first_name")
    serializer_class = ActorSerializer