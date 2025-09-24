


from rest_framework import status
from rest_framework.reverse import reverse

from ...models import Theme
from ...tests.test_themes import TestThemes, NOT_FOUND_ID


class DeleteThemeTestCase(TestThemes):
    """
    Tests pour l'endpoint DELETE /api/themes/<id>/ (suppression d'un thème).
    """
    def test_delete_theme_success(self):
        """
        Vérifie qu'un thème existant peut être supprimé avec succès.
        """
        delete_url = reverse('theme-detail', args=[self.parent_theme.id])
        response = self.client.delete(delete_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Theme.objects.filter(id=self.parent_theme.id).exists())

    def test_delete_theme_nonexistent(self):
        """
        Vérifie qu'une erreur 404 est renvoyée si l'ID du thème n'existe pas.
        """
        delete_url = reverse('theme-detail', args=[NOT_FOUND_ID])
        response = self.client.delete(delete_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_theme_unauthenticated(self):
        """
        Vérifie qu'une erreur 401 est renvoyée si l'utilisateur n'est pas authentifié.
        """
        self.client.logout()
        delete_url = reverse('theme-detail', args=[self.parent_theme.id])
        response = self.client.delete(delete_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
