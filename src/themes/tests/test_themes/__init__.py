# python manage.py test quiz.tests.test_themes

from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from ...models import Theme

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
