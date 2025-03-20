
from rest_framework import serializers

from quiz.models import Question


class QuestionPlaySerializer(serializers.ModelSerializer):
    answer_synonyms = serializers.ReadOnlyField()
    choices = serializers.ReadOnlyField()
    theme = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'correct_answer', 'theme', 'explanation',
            'difficulty', 'answer_synonyms','choices', 'accept_close_answer',
        ]
        read_only_fields = ['id']

    def get_theme(self, obj):
        return obj.theme.name


class QuestionCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'theme', 'question_text', 'question_type', 'correct_answer', 'accept_close_answer',
            'difficulty', 'fake_answer_1', 'fake_answer_2', 'fake_answer_3', 'explanation'
        ]
        read_only_fields = ['id']
