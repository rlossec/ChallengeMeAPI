# python manage.py test quiz.tests.test_favorites

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

from django.contrib.auth import get_user_model

from quiz.models import Theme

User = get_user_model()


class FavoritesEndpointsTestCase(APITestCase):
    def setUp(self):
        # Création d'un utilisateur et connexion
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Création de thèmes
        self.theme1 = Theme.objects.create(name="Arts et Littératures", description="", color="#8c348d", order=3)
        self.theme2 = Theme.objects.create(name="Sciences", description="", color="#123456", order=1)


    def add_favorite(self, theme_id):
        self.client.post(reverse('add-favorite', args=[theme_id]))

    def remove_favorite(self, theme_id):
        self.client.delete(reverse('remove-favorite', args=[theme_id]))

    def test_authentication_required(self):
        """
        Vérifie que les endpoints nécessitent une authentification.
        """
        self.client.logout()

        # Tester accès non authentifié pour chaque endpoint
        response = self.client.get(reverse('favorite-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

        response = self.client.post(reverse('add-favorite', args=[self.theme1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

        response = self.client.delete(reverse('remove-favorite', args=[self.theme1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
