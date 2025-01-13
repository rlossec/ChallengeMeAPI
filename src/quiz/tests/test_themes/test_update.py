

from quiz.tests.test_themes import TestThemes, NOT_FOUND_ID

from rest_framework import status
from rest_framework.reverse import reverse


# -- PATCH /api/themes/<id>/ --
class UpdateThemeTestCase(TestThemes):
    """

    """
    # 401 Non authentifié
    def test_update_theme_unauthenticated(self):
        """
        Vérifie qu'une erreur 401 est renvoyée si l'utilisateur n'est pas authentifié.
        """
        self.client.logout()  # Supprime l'authentification
        update_url = reverse('theme-detail', args=[self.parent_theme.id])
        data = {"name": "Unauthenticated Update"}
        response = self.client.patch(update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 200 Succès
    def test_update_theme_success(self):
        """
        Vérifie qu'un thème est mis à jour avec succès avec des données valides.
        """
        update_url = reverse('theme-detail', args=[self.parent_theme.id])
        data = {
            "name": "Updated Parent Theme",
            "description": "Updated description",
            "color": "#123456",
            "order": 10
        }
        response = self.client.patch(update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérification des mises à jour
        self.parent_theme.refresh_from_db()
        self.assertEqual(self.parent_theme.name, "Updated Parent Theme")
        self.assertEqual(self.parent_theme.description, "Updated description")
        self.assertEqual(self.parent_theme.color, "#123456")
        self.assertEqual(self.parent_theme.order, 10)

    def test_update_theme_partial_success(self):
        """
        Vérifie qu'une mise à jour partielle fonctionne.
        """
        update_url = reverse('theme-detail', args=[self.parent_theme.id])
        data = {"name": "Partially Updated Theme"}
        response = self.client.patch(update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérification des mises à jour partielles
        self.parent_theme.refresh_from_db()
        self.assertEqual(self.parent_theme.name, "Partially Updated Theme")
        self.assertIsNone(self.parent_theme.description)  # Non modifié
        self.assertEqual(self.parent_theme.order, 0)  # Non modifié

    # 400 Mauvaise requête
    def test_update_theme_invalid_field(self):
        """
        Vérifie qu'une erreur 400 est renvoyée si un champ invalide est fourni.
        """
        update_url = reverse('theme-detail', args=[self.parent_theme.id])
        data = {"name": ""}
        response = self.client.patch(update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_update_theme_invalid_parent(self):
        """
        Vérifie qu'une erreur 400 est renvoyée si `parent_theme` contient un ID inexistant.
        """
        update_url = reverse('theme-detail', args=[self.parent_theme.id])
        data = {"parent_theme": NOT_FOUND_ID}
        response = self.client.patch(update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("parent_theme", response.data)

    def test_update_nonexistent_theme(self):
        """
        Vérifie qu'une erreur 404 est renvoyée si l'ID du thème n'existe pas.
        """
        update_url = reverse('theme-detail', args=[NOT_FOUND_ID])
        data = {"name": "Nonexistent Theme"}
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
