from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DashboardAuthTests(TestCase):
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
            fetch_redirect_response=False,
        )

    def test_categories_requires_login(self):
        response = self.client.get(reverse('categories'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('categories')}",
            fetch_redirect_response=False,
        )

    def test_authenticated_user_can_access_dashboard(self):
        user = User.objects.create_user(username='dashboard-user', password='test-pass-123')
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
