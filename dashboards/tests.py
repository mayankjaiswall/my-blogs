from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blogs.models import Category


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

    def test_category_crud_requires_login(self):
        category = Category.objects.create(category_name='Tech')

        protected_urls = [
            reverse('add_category'),
            reverse('edit_category', args=[category.id]),
            reverse('delete_category', args=[category.id]),
        ]

        for url in protected_urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={url}",
                    fetch_redirect_response=False,
                )

    def test_authenticated_user_can_access_dashboard(self):
        user = User.objects.create_user(username='dashboard-user', password='test-pass-123')
        self.client.force_login(user)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_add_category(self):
        user = User.objects.create_user(username='category-user', password='test-pass-123')
        self.client.force_login(user)

        response = self.client.post(reverse('add_category'), {'category_name': 'News'})

        self.assertRedirects(response, reverse('categories'))
        self.assertTrue(Category.objects.filter(category_name='News').exists())

    def test_authenticated_user_can_edit_category(self):
        user = User.objects.create_user(username='category-editor', password='test-pass-123')
        category = Category.objects.create(category_name='Old Name')
        self.client.force_login(user)

        response = self.client.post(
            reverse('edit_category', args=[category.id]),
            {'category_name': 'New Name'},
        )

        category.refresh_from_db()
        self.assertRedirects(response, reverse('categories'))
        self.assertEqual(category.category_name, 'New Name')

    def test_authenticated_user_can_delete_category(self):
        user = User.objects.create_user(username='category-deleter', password='test-pass-123')
        category = Category.objects.create(category_name='Temporary')
        self.client.force_login(user)

        response = self.client.post(reverse('delete_category', args=[category.id]))

        self.assertRedirects(response, reverse('categories'))
        self.assertFalse(Category.objects.filter(id=category.id).exists())
