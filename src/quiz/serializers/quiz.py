
from rest_framework import serializers
from quiz.models import ClassicQuiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassicQuiz
        fields = ["id", "creator", "themes", "is_temporary_quiz", "created_at"]
