
from django.contrib.auth import get_user_model

from rest_framework import status

from accounts.tests import MANDATORY_FIELD_ERROR_MESSAGE
from ...models import Theme
from ...tests.test_themes import TestThemes, NOT_FOUND_ID

User = get_user_model()

# -- POST /api/themes/ --
class CreateThemeTestCase(TestThemes):
    """
    Tests pour l'endpoint POST /api/themes/ (création de thème).
    """

    # 401 Non authentifié
    def test_create_theme_unauthenticated(self):
        """
        Vérifie qu'une erreur 401 est renvoyée si l'utilisateur n'est pas authentifié.
        """
        self.client.logout()
        initial_themes_count = Theme.objects.count()
        data = {"name": "Unauthenticated Theme"}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Theme.objects.count(), initial_themes_count)

    # 200 - Succès
    def test_create_theme(self):
        """
        Test de la création d'un nouveau thème.
        """
        data = {
            "name": "New Theme",
            "description": "Description of new theme",
            "parent_theme": None,
            "color": "#FF5733",
            "order": 3
        }
        initial_themes_count = Theme.objects.count()
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Theme.objects.count(), initial_themes_count + 1)
        self.assertEqual(Theme.objects.last().name, "New Theme")

    def test_create_theme_optional_fields(self):
        """
        Vérifie qu'on peut créer un thème avec ou sans les champs facultatifs.
        """
        # Cas avec uniquement le champ obligatoire
        data = {"name": "Minimal Theme"}
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Theme.objects.last().name, "Minimal Theme")
        self.assertIsNone(Theme.objects.last().description)
        self.assertIsNone(Theme.objects.last().parent_theme)
        self.assertIsNone(Theme.objects.last().color)

        # Cas avec tous les champs remplis
        data = {
            "name": "Full Theme",
            "description": "A fully described theme",
            "parent_theme": self.parent_theme.id,
            "color": "#123456",
            "order": 5
        }
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Theme.objects.last().name, "Full Theme")
        self.assertEqual(Theme.objects.last().description, "A fully described theme")
        self.assertEqual(Theme.objects.last().color, "#123456")

    # 400 Mauvaise requête
    def test_create_theme_missing_name(self):
        """
        Vérifie qu'une erreur 400 est renvoyée si le champ `name` est manquant.
        """
        initial_themes_count = Theme.objects.count()
        data = {
            "description": "Description without name",
            "parent_theme": self.parent_theme.id,
            "color": "#FF5733",
            "order": 1
        }
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Theme.objects.count(), initial_themes_count)
        self.assertIn("name", response.data)
        self.assertIn(MANDATORY_FIELD_ERROR_MESSAGE, response.data["name"])

    def test_create_theme_invalid_parent_theme(self):
        """
        Vérifie qu'une erreur 404 est renvoyée si le champ `parent_theme` contient un ID inexistant.
        """
        initial_themes_count = Theme.objects.count()
        data = {
            "name": "Invalid Parent Theme",
            "parent_theme": NOT_FOUND_ID
        }
        response = self.client.post(self.base_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Theme.objects.count(), initial_themes_count)  # Aucun thème n'est créé
        self.assertIn("parent_theme", response.data)

