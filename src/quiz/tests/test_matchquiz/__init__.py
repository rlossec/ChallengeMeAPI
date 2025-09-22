# python manage.py test quiz.tests.test_matchquiz

from django.urls import reverse

from rest_framework.test import APITestCase
from quiz.models import MatchQuiz, Theme, MatchPair
from django.contrib.auth import get_user_model

User = get_user_model()


class TestMatchQuiz(APITestCase):
    def setUp(self):
        # Création d'un utilisateur principal
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="ValidPassword123!",
        )

        # Création d'un autre utilisateur
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@example.com",
            password="AnotherValidPassword123!",
        )

        # Création de plusieurs thèmes
        self.themes = [
            Theme.objects.create(name="Theme 1"),
            Theme.objects.create(name="Theme 2"),
            Theme.objects.create(name="Theme 3"),
        ]

        # Création d'un quiz principal avec des paires et des thèmes associés
        self.match_quiz = MatchQuiz.objects.create(
            title="Initial Quiz Title",
            difficulty=4,
            text="Initial Quiz Description",
            valid=True,
            creator=self.user,
        )
        self.match_quiz.themes.set(self.themes[:2])  # Associer les deux premiers thèmes

        # Ajout de paires au quiz
        self.pairs = [
            MatchPair.objects.create(
                match_quiz=self.match_quiz,
                text_clue="Indice 1",
                answer="Réponse 1",
            ),
            MatchPair.objects.create(
                match_quiz=self.match_quiz,
                picture_clue="image1.jpg",
                answer="Réponse 2",
            ),
        ]

        # Création d'autres quizzes pour les tests
        self.other_quizzes = [
            MatchQuiz.objects.create(
                title=f"Quiz {i}",
                difficulty=i,
                text=f"Description du quiz {i}",
                valid=False,
                creator=self.user if i % 2 == 0 else self.other_user,
            )
            for i in range(1, 4)  # Crée trois autres quizzes
        ]

        self.match_quiz_update_url = reverse("matchquiz-detail", kwargs={"pk": self.match_quiz.id})

