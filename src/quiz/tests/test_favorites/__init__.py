# python manage.py test quiz.tests.test_favorites

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

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

        # URL pour les tests
        self.list_favorites_url = reverse('favorite-list')
        self.add_favorite_url = reverse('add-favorite',  args=[self.theme1.pk])
        self.remove_favorite_url = reverse('remove-favorite',  args=[self.theme1.pk])
