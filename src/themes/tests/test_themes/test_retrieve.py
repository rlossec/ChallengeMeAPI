
from rest_framework import status
from rest_framework.reverse import reverse

from ...tests.test_themes import TestThemes, NOT_FOUND_ID


class RetrieveThemeTestCase(TestThemes):
    """
    Tests pour l'endpoint GET /api/themes/<id>/ (récupération d'un thème).
    """
    def test_retrieve_theme_success(self):
        """
        Vérifie qu'un thème existant peut être récupéré avec succès.
        """
        retrieve_url = reverse('theme-detail', args=[self.parent_theme.id])
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.parent_theme.id)
        self.assertEqual(response.data['name'], self.parent_theme.name)
        self.assertEqual(response.data['description'], self.parent_theme.description)

    def test_retrieve_theme_nonexistent(self):
        """
        Vérifie qu'une erreur 404 est renvoyée si l'ID du thème n'existe pas.
        """
        retrieve_url = reverse('theme-detail', args=[NOT_FOUND_ID])
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_theme_unauthenticated(self):
        """
        Vérifie qu'une erreur 401 est renvoyée si l'utilisateur n'est pas authentifié.
        """
        self.client.logout()
        retrieve_url = reverse('theme-detail', args=[self.parent_theme.id])
        response = self.client.get(retrieve_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
