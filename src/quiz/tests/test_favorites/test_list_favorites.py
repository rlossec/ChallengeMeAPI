
from rest_framework import status

from quiz.tests.test_favorites import FavoritesEndpointsTestCase


class TestListFavorites(FavoritesEndpointsTestCase):
    def test_list_favorites(self):
        """
        Teste la liste des thèmes favoris de l'utilisateur.
        """
        # Ajout de theme1 aux favoris
        self.client.post(self.add_favorite_url)

        # Récupération de la liste des favoris
        response = self.client.get(self.list_favorites_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.theme1.id)
