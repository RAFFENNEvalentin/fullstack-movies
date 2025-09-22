from typing import Optional
from django.db.models import Avg, Prefetch, QuerySet
from movies.models import Movie, Actor

"""
Améliorations possibles (si plus de temps) :
- Interface (Protocol) pour le repository
- Implémentation par défaut via ORM Django
- Registry pour sélectionner l’impl via un setting (MOVIE_REPOSITORY_IMPL)
- Bénéfices : switch de backend (Postgres/SQL brut/service), mocks en tests unitaires
"""

class MovieRepository:
    @staticmethod
    def list_all() -> QuerySet[Movie]:
        return (
            Movie.objects
            # .only("id", "title", "description")  # optionnel
            .all()
            .prefetch_related(
                Prefetch("actors", queryset=Actor.objects.only("id", "first_name", "last_name"))
            )
            .annotate(average_grade=Avg("reviews__grade"))
        )

    @staticmethod
    def get_by_id(movie_id: int) -> Optional[Movie]:
        return (
            Movie.objects
            .filter(id=movie_id)
            # .only("id", "title", "description")  # optionnel
            .prefetch_related(
                Prefetch("actors", queryset=Actor.objects.only("id", "first_name", "last_name"))
            )
            .annotate(average_grade=Avg("reviews__grade"))
            .first()
        )