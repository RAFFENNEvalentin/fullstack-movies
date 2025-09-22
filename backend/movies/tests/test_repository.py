from django.test import TestCase
from movies.models import Movie, Actor, Review
from movies.repositories.movie_repository import MovieRepository

class MovieRepositoryTests(TestCase):
    def setUp(self):
        a1 = Actor.objects.create(first_name="Tom", last_name="Hanks")
        a2 = Actor.objects.create(first_name="Natalie", last_name="Portman")
        m  = Movie.objects.create(title="Big")
        m.actors.add(a1, a2)
        Review.objects.create(movie=m, grade=5)
        Review.objects.create(movie=m, grade=3)

    def test_list_all_annotates_average_grade(self):
        qs = MovieRepository.list_all()
        m = qs.first()
        self.assertIsNotNone(m)
        self.assertAlmostEqual(m.average_grade, 4.0)
        self.assertEqual(m.actors.count(), 2)

    def test_get_by_id_returns_movie(self):
        m = Movie.objects.first()
        got = MovieRepository.get_by_id(m.id)
        self.assertIsNotNone(got)
        self.assertEqual(got.id, m.id)