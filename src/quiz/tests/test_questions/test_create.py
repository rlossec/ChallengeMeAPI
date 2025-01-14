
from rest_framework import status

from quiz.tests.test_questions import TestQuestions, NOT_FOUND_ID
from quiz.models import Question


class CreateQuestionTestCase(TestQuestions):

    # 401 Non authentifié
    def test_create_question_unauthenticated(self):
        """
        Vérifie qu'une erreur 401 est retournée si l'utilisateur n'est pas authentifié.
        """
        initial_questions_count = Question.objects.count()
        self.client.logout()
        data = {
            "theme": self.parent_theme.id,
            "question_text": "New question text",
            "question_type": "text",
            "correct_answer": "Answer",
            "explanation": "Explanation of the answer",
            "difficulty": 1.5,
        }
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Question.objects.count(), initial_questions_count)

    # 200
    def test_create_question_success(self):
        """
        Test de création réussie d'une question.
        """
        initial_questions_count = Question.objects.count()
        data = {
            "theme": self.parent_theme.id,
            "question_text": "New question text",
            "question_type": "text",
            "correct_answer": "Answer",
            "explanation": "Explanation of the answer",
            "difficulty": 1.5,
        }
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), initial_questions_count + 1)

    # 400

    def test_create_question_missing_field(self):
        """
        Vérifie qu'une erreur 400 est retournée si un champ obligatoire est manquant.
        """
        initial_questions_count = Question.objects.count()
        required_fields = [
            "theme",
            "question_type",
            "correct_answer",
            "question_text",
        ]

        for field in required_fields:
            with self.subTest(missing_field=field):
                data = {
                    "theme": self.parent_theme.id,
                    "question_type": "text",
                    "correct_answer": "Answer",
                    "question_text": "question",
                    "accept_close_answer": False,
                }
                # Supprimer le champ manquant
                data.pop(field)

                response = self.client.post(self.base_url, data, format='json')

                # Vérifier que le statut est 400 BAD REQUEST
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                    f"Le statut attendu est 400 quand le champ {field} est manquant."
                )
                # Vérifier que le champ manquant est mentionné dans la réponse
                self.assertIn(
                    field,
                    response.data,
                    f"Le champ {field} manquant devrait être mentionné dans la réponse."
                )
                # Vérifier qu'aucune nouvelle question n'est créée
                self.assertEqual(
                    Question.objects.count(),
                    initial_questions_count,
                    "Aucune nouvelle question ne devrait être créée si un champ est manquant."
                )

    def test_create_question_invalid_theme(self):
        """
        Vérifie qu'une erreur 400 est retournée si le thème fourni est invalide.
        """
        initial_questions_count = Question.objects.count()
        data = {
            "theme": NOT_FOUND_ID,
            "question_text": "New question text",
            "question_type": "text",
            "correct_answer": "Answer",
            "explanation": "Explanation of the answer",
            "difficulty": 1.5,
        }
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Question.objects.count(), initial_questions_count)
