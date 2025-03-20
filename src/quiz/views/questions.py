from rest_framework.viewsets import ModelViewSet
from ..models import Question
from ..serializers import QuestionPlaySerializer, QuestionCRUDSerializer


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionPlaySerializer

    def get_serializer_class(self):
        """
        Retourne le sérialiseur approprié en fonction de l'action.
        """
        if self.action == "create" or self.action == "update":
            return QuestionCRUDSerializer
        return QuestionCRUDSerializer
