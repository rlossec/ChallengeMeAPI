# python manage.py test quiz.tests.test_questions

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from django.contrib.auth import get_user_model

from quiz.models import Theme, Question

User = get_user_model()
NOT_FOUND_ID = 9999999999


class TestQuestions(APITestCase):
    def setUp(self):
        # Création d'un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='ValidPassword123!',
            first_name='John',
            last_name='Doe'
        )
        self.client.force_authenticate(self.user)

        # Création de thèmes pour les tests
        self.parent_theme = Theme.objects.create(name="Parent Theme")
        self.subtheme1 = Theme.objects.create(name="Subtheme 1", parent_theme=self.parent_theme, order=0)
        self.subtheme2 = Theme.objects.create(name="Subtheme 2", parent_theme=self.parent_theme, order=1)
        self.subtheme3 = Theme.objects.create(name="Subtheme 3", parent_theme=self.parent_theme, order=2)

        # URL de base pour les tests
        self.base_url = reverse('theme-list')  # Route pour lister/créer des thèmes
        self.detail_url = reverse('theme-detail', args=[self.parent_theme.id])  # Route pour un thème spécifique

        # Ajout de questions pour les tests
        self.question1 = Question.objects.create(
            theme=self.parent_theme,
            question_text="What is the capital of France?",
            question_type="text",
            correct_answer="Paris",
            explanation="Paris is the capital of France.",
            difficulty=1.0,
        )
        self.question2 = Question.objects.create(
            theme=self.subtheme1,
            question_text="What is 2+2?",
            question_type="multiple_choice",
            correct_answer="4",
            fake_answer_1="3",
            fake_answer_2="5",
            fake_answer_3="22",
            difficulty=0.5,
        )
        self.base_url = reverse('question-list')
