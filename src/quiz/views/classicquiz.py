
from rest_framework import viewsets

from quiz.models import ClassicQuiz
from quiz.serializers import ClassicQuizSerializer


class ClassicQuizViewSet(viewsets.ModelViewSet):
    queryset = ClassicQuiz.objects.all()
    serializer_class = ClassicQuizSerializer
