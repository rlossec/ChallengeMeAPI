
from rest_framework import serializers

from quiz.models import ClassicQuiz
from quiz.serializers import QuestionPlaySerializer


class ClassicQuizSerializer(serializers.ModelSerializer):
    questions = QuestionPlaySerializer(many=True)
    themes = serializers.SerializerMethodField()

    class Meta:
        model = ClassicQuiz
        fields = ["id", "title", 'type', "difficulty", "themes", "questions"]

    def get_themes(self, obj):
        themes = obj.themes.all()
        return [theme.name for theme in themes]
