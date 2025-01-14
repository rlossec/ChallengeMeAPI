from rest_framework import status
from rest_framework.reverse import reverse

from quiz.tests.test_questions import TestQuestions, NOT_FOUND_ID


class RetrieveQuestionTestCase(TestQuestions):
    def test_retrieve_question_success(self):
        """
        Vérifie qu'une question existante peut être récupérée.
        """
        retrieve_url = reverse('question-detail', args=[self.question1.id])
        response = self.client.get(retrieve_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question1.id)
        self.assertEqual(response.data['question_text'], self.question1.question_text)
        self.assertEqual(response.data['choices'], self.question1.choices)

    def test_retrieve_question_not_found(self):
        """
        Vérifie qu'une erreur 404 est retournée si l'ID de la question n'existe pas.
        """
        retrieve_url = reverse('question-detail', args=[NOT_FOUND_ID])
        response = self.client.get(retrieve_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
