
from rest_framework import status

from quiz.tests.test_favorites import FavoritesEndpointsTestCase


class TestRemoveFavorite(FavoritesEndpointsTestCase):

    def test_remove_favorite_in_favorites(self):
        """
        Teste la suppression d'un thème présent dans les favoris.
        """
        # Ajout initial du thème
        self.client.post(self.add_favorite_url)

        # Suppression du thème
        response = self.client.delete(self.remove_favorite_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Theme removed from favorites.")

    def test_remove_favorite_not_in_favorites(self):
        """
        Teste la suppression d'un thème non présent dans les favoris.
        """
        response = self.client.delete(self.remove_favorite_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Theme not in favorites.")
