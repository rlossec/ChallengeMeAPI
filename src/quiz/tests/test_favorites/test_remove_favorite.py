
from rest_framework import status
from rest_framework.reverse import reverse

from quiz.tests.test_favorites import FavoritesEndpointsTestCase
from quiz.tests.test_themes import NOT_FOUND_ID


class TestRemoveFavorite(FavoritesEndpointsTestCase):

    # 200
    def test_remove_favorite_in_favorites(self):
        """
        Teste la suppression d'un thème présent dans les favoris.
        """
        # Ajout initial du thème
        THEME_ID = self.theme1.id
        self.add_favorite(THEME_ID)

        # Suppression du thème
        response = self.client.delete(reverse('remove-favorite', args=[THEME_ID]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Theme removed from favorites.")

    # 400
    def test_remove_favorite_not_in_favorites(self):
        """
        Teste la suppression d'un thème non présent dans les favoris.
        """
        THEME_ID = self.theme1.id
        response = self.client.delete(reverse('remove-favorite', args=[THEME_ID]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Theme not in favorites.")

    # 404
    def test_remove_favorite_inexistant_theme_id(self):
        """
        Teste la suppression d'un favori avec un ID de thème invalide.
        """
        response = self.client.delete(reverse('remove-favorite', args=[NOT_FOUND_ID]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Theme not found.")

