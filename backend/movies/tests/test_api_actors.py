# backend/movies/tests/test_api_actors.py
from django.test import TestCase
from rest_framework.test import APIClient
from movies.models import Actor

class ActorsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Actor.objects.create(first_name="Tom", last_name="Hanks")
        Actor.objects.create(first_name="Natalie", last_name="Portman")

    def test_list_actors(self):
        resp = self.client.get("/api/actors/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # Réponse paginée
        self.assertIn("count", data)
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        self.assertGreaterEqual(len(data["results"]), 2)
        self.assertIn("first_name", data["results"][0])
        self.assertIn("last_name", data["results"][0])