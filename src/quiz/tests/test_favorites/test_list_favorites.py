
from rest_framework import status
from rest_framework.reverse import reverse

from quiz.models import Theme
from quiz.tests.test_favorites import FavoritesEndpointsTestCase


class TestListFavorites(FavoritesEndpointsTestCase):

    def setUp(self):
        super().setUp()
        self.list_favorites_url = reverse('favorite-list')

    # 200
    def test_list_favorites(self):
        """
        Teste la liste des thèmes favoris de l'utilisateur.
        """
        # Ajout de theme1 aux favoris
        self.add_favorite(self.theme1.pk)

        # Récupération de la liste des favoris
        favorites_count = Theme.objects.filter(favorited_by__user=self.user).count()
        response = self.client.get(self.list_favorites_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), favorites_count)
        self.assertEqual(response.data[0]["id"], self.theme1.id)

    def test_list_favorites_empty(self):
        """
        Vérifie que la liste des favoris est vide au départ.
        """
        response = self.client.get(self.list_favorites_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
