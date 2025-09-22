from django.test import SimpleTestCase

class HealthCheckTests(SimpleTestCase):
    def test_health_returns_ok(self):
        resp = self.client.get("/api/health/")
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {"status": "ok"})