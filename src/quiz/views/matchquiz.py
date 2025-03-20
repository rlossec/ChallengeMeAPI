
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from quiz.models import MatchQuiz
from quiz.serializers import MatchQuizSerializer, MatchQuizCRUDSerializer


class MatchQuizViewSet(viewsets.ModelViewSet):
    queryset = MatchQuiz.objects.all()

    def get_serializer_class(self):
        # Utiliser un serializer différent pour les actions create et update
        if self.action in ["create", "update", "partial_update"]:
            return MatchQuizCRUDSerializer
        return MatchQuizSerializer

    @action(detail=True, methods=["get"])
    def for_edit(self, request, pk=None):
        """Endpoint spécifique pour récupérer le quiz dans le contexte d'édition"""
        quiz = self.get_object()
        serializer = MatchQuizCRUDSerializer(quiz)
        return Response(serializer.data)