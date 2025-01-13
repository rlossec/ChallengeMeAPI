
from rest_framework import status

from quiz.tests.test_favorites import FavoritesEndpointsTestCase


class TestAddFavorite(FavoritesEndpointsTestCase):
    def test_add_favorite_not_in_favorites(self):
        """
        Teste l'ajout d'un thème non présent dans les favoris.
        """
        response = self.client.post(self.add_favorite_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "Theme added to favorites.")

    def test_add_favorite_already_in_favorites(self):
        """
        Teste l'ajout d'un thème déjà présent dans les favoris.
        """
        # Ajout initial du thème
        self.client.post(self.add_favorite_url)

        # Tentative d'ajout du même thème
        response = self.client.post(self.add_favorite_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Theme already in favorites.")