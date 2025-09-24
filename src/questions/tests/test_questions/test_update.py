
from rest_framework import status
from rest_framework.reverse import reverse

from ..test_questions import TestQuestions


class UpdateQuestionTestCase(TestQuestions):
    def test_update_question_success(self):
        """
        Vérifie qu'une question existante peut être mise à jour avec succès.
        """
        update_url = reverse('question-detail', args=[self.question1.id])
        data = {"question_text": "Updated question text"}
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question1.refresh_from_db()
        self.assertEqual(self.question1.question_text, "Updated question text")

    def test_update_question_invalid_data(self):
        """
        Vérifie qu'une erreur 400 est retournée si les données de mise à jour sont invalides.
        """
        update_url = reverse('question-detail', args=[self.question1.id])
        data = {"difficulty": "invalid_float"}  # Mauvais type de données
        response = self.client.patch(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

