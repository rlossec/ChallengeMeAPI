
from rest_framework import status

from ...models import Question
from ..test_questions import NOT_FOUND_ID, TestQuestions


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
            "question_type": "TXT",
            "correct_answer": "Answer",
            "explanation": "Explanation of the answer",
            "difficulty": 1.5,
        }
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), initial_questions_count + 1)

    # 400
    def test_create_question_invalid_theme(self):
        """
        Vérifie qu'une erreur 400 est retournée si le thème fourni est invalide.
        """
        initial_questions_count = Question.objects.count()
        data = {
            "theme": NOT_FOUND_ID,
            "question_text": "New question text",
            "question_type": "TXT",
            "correct_answer": "Answer",
            "explanation": "Explanation of the answer",
            "difficulty": 1.5,
        }
        response = self.client.post(self.base_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Question.objects.count(), initial_questions_count)
