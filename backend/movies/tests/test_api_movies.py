from django.test import TestCase
from rest_framework.test import APIClient
from movies.models import Movie, Actor, Review

class MoviesApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Acteurs
        self.a1 = Actor.objects.create(first_name="Tom", last_name="Hanks")
        self.a2 = Actor.objects.create(first_name="Natalie", last_name="Portman")
        # 6 films (pour tester pagination=5)
        self.m1 = Movie.objects.create(title="M1")
        self.m2 = Movie.objects.create(title="M2")
        self.m3 = Movie.objects.create(title="M3")
        self.m4 = Movie.objects.create(title="M4")
        self.m5 = Movie.objects.create(title="M5")
        self.m6 = Movie.objects.create(title="M6")
        # Liaisons + reviews pour m1 (moyenne = 4.0)
        self.m1.actors.add(self.a1, self.a2)
        Review.objects.create(movie=self.m1, grade=5)
        Review.objects.create(movie=self.m1, grade=3)

    def test_list_is_paginated_by_5(self):
        resp = self.client.get("/api/movies/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("count", data)
        self.assertIn("results", data)
        self.assertEqual(data["count"], 6)
        self.assertEqual(len(data["results"]), 5)

    def test_retrieve_contains_actors_and_average_grade(self):
        resp = self.client.get(f"/api/movies/{self.m1.id}/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["id"], self.m1.id)
        self.assertEqual(len(data["actors"]), 2)
        self.assertAlmostEqual(data["average_grade"], 4.0)

    def test_post_review_valid_and_invalid(self):
        url = f"/api/movies/{self.m1.id}/reviews/"
        # invalide (0) -> 400 (validators modèle)
        bad = self.client.post(url, {"grade": 0}, format="json")
        self.assertEqual(bad.status_code, 400)
        # valide (5) -> 201
        ok = self.client.post(url, {"grade": 5}, format="json")
        self.assertEqual(ok.status_code, 201)

    def test_patch_movie_updates_description_and_actors(self):
        url = f"/api/movies/{self.m2.id}/"
        payload = {"description": "Updated", "actor_ids": [self.a1.id]}
        resp = self.client.patch(url, payload, format="json")
        self.assertEqual(resp.status_code, 200)
        self.m2.refresh_from_db()
        self.assertEqual(self.m2.description, "Updated")
        self.assertEqual(self.m2.actors.count(), 1)
        self.assertEqual(self.m2.actors.first().id, self.a1.id)