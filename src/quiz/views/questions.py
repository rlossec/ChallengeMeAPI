from rest_framework.viewsets import ModelViewSet
from ..models import Question
from ..serializers import QuestionSerializer, QuestionCreateUpdateSerializer


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_serializer_class(self):
        """
        Retourne le sérialiseur approprié en fonction de l'action.
        """
        if self.action == "create" or self.action == "update":
            return QuestionCreateUpdateSerializer
        return QuestionSerializer
