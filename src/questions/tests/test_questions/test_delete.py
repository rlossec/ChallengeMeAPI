from rest_framework import status
from rest_framework.reverse import reverse

from ..test_questions import NOT_FOUND_ID, TestQuestions
from ...models import Question


class DeleteQuestionTestCase(TestQuestions):
    def test_delete_question_success(self):
        """
        Vérifie qu'une question existante peut être supprimée avec succès.
        """
        delete_url = reverse('question-detail', args=[self.question1.id])
        response = self.client.delete(delete_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Question.objects.filter(id=self.question1.id).exists())

    def test_delete_question_not_found(self):
        """
        Vérifie qu'une erreur 404 est retournée si l'ID de la question n'existe pas.
        """
        delete_url = reverse('question-detail', args=[NOT_FOUND_ID])
        response = self.client.delete(delete_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
