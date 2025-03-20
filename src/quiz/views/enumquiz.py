
from rest_framework import viewsets

from quiz.models import EnumQuiz
from quiz.serializers import EnumQuizSerializer


class EnumQuizViewSet(viewsets.ModelViewSet):
    queryset = EnumQuiz.objects.all()
    serializer_class = EnumQuizSerializer
