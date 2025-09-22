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
        # Réponse = liste directe (pas paginée)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)
        self.assertIn("first_name", data[0])
        self.assertIn("last_name", data[0])