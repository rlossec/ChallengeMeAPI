# python manage.py test quiz.tests.test_themes

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from accounts.tests import MANDATORY_FIELD_ERROR_MESSAGE
from quiz.models import Theme

User = get_user_model()
NOT_FOUND_ID = 9999999999

class TestThemes(APITestCase):
    """
    Classe de base pour initialiser les données nécessaires aux tests.
    """
    def setUp(self):
        # Création d'un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='ValidPassword123!',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(self.user)  # Authentification automatique pour les tests

        # Création de thèmes pour les tests
        self.parent_theme = Theme.objects.create(name="Parent Theme")
        self.subtheme1 = Theme.objects.create(name="Subtheme 1", parent_theme=self.parent_theme, order=0)
        self.subtheme2 = Theme.objects.create(name="Subtheme 2", parent_theme=self.parent_theme, order=1)
        self.subtheme3 = Theme.objects.create(name="Subtheme 3", parent_theme=self.parent_theme, order=2)

        # URL de base pour les tests
        self.base_url = reverse('theme-list')  # Route pour lister/créer des thèmes
        self.detail_url = reverse('theme-detail', args=[self.parent_theme.id])  # Route pour un thème spécifique


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


class ReorderSubthemesTestCase(TestThemes):

    # -- POST /api/themes/<theme_id>/reorder_subthemes/ -- #
    def test_reorder_subthemes_success(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": [self.subtheme3.id, self.subtheme1.id, self.subtheme2.id]}

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "L'ordre des sous-thèmes a été mis à jour avec succès.")

        # Vérifie que l'ordre a bien été mis à jour
        self.subtheme1.refresh_from_db()
        self.subtheme2.refresh_from_db()
        self.subtheme3.refresh_from_db()

        self.assertEqual(self.subtheme1.order, 1)
        self.assertEqual(self.subtheme2.order, 2)
        self.assertEqual(self.subtheme3.order, 0)

    def test_reorder_subthemes_invalid_subtheme(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": [NOT_FOUND_ID, self.subtheme1.id]}

        self.client.force_authenticate(self.user)
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Certains sous-thèmes ne correspondent pas", response.data['error'])

    def test_reorder_subthemes_with_subtheme_not_in_parent(self):
        other_theme = Theme.objects.create(name="Other Theme")
        url = f"/api/themes/{self.parent_theme.id}/reorder_subthemes/"
        payload = {"subtheme_order": [self.subtheme1.id, other_theme.id]}  # other_theme est invalide

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Certains sous-thèmes ne correspondent pas", response.data['error'])

    def test_reorder_subthemes_empty_list(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": []}

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This list may not be empty.', response.data['subtheme_order'])

    def test_reorder_subthemes_invalid_data_type(self):
        url = reverse('theme-reorder-subthemes', args=[self.parent_theme.id])
        payload = {"subtheme_order": "not_a_list"}  # Mauvais type de données

        self.client.force_authenticate(self.user)

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Expected a list of items but got type "str".', response.data['subtheme_order'])
