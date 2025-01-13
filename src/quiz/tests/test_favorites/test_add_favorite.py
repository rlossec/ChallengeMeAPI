
from rest_framework import status
from rest_framework.reverse import reverse

from quiz.tests.test_favorites import FavoritesEndpointsTestCase
from quiz.tests.test_questions import NOT_FOUND_ID


class TestAddFavorite(FavoritesEndpointsTestCase):
    # 200
    def test_add_favorite_not_in_favorites(self):
        """
        Teste l'ajout d'un thème non présent dans les favoris.
        """
        response = self.client.post(reverse('add-favorite', args=[self.theme1.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["detail"], "Theme added to favorites.")

    # 400
    def test_add_favorite_already_added(self):
        """
        Vérifie qu'un favori déjà ajouté ne peut pas être ajouté à nouveau.
        """
        THEME_ID = self.theme1.id
        self.add_favorite(THEME_ID)                                                       # Ajouter une première fois
        response = self.client.post(reverse('add-favorite', args=[THEME_ID]))    # Ajouter une deuxième fois
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Theme already in favorites.")

    # 404
    def test_add_favorite_inexistant_theme_id(self):
        """
        Teste l'ajout d'un favori avec un ID de thème invalide.
        """
        response = self.client.post(reverse('add-favorite', args=[NOT_FOUND_ID]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Theme not found.")


