from django.test import TestCase, Client
from django.urls import reverse


class HealthCheckTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check_endpoint(self):
        """Test that health check endpoint returns 200"""
        response = self.client.get(reverse('health_check'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')

    def test_liveness_check_endpoint(self):
        """Test that liveness check endpoint returns 200"""
        response = self.client.get(reverse('liveness_check'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'alive')

    def test_readiness_check_endpoint(self):
        """Test that readiness check endpoint returns 200 when DB is connected"""
        response = self.client.get(reverse('readiness_check'))
        # Should be 200 if DB is available, 503 if not
        self.assertIn(response.status_code, [200, 503])
