
from rest_framework import serializers

from quiz.models import Question
from quiz.serializers import ThemeSerializer


class QuestionSerializer(serializers.ModelSerializer):
    answer_synonyms = serializers.ReadOnlyField()
    choices = serializers.ReadOnlyField()
    theme = ThemeSerializer()

    class Meta:
        model = Question
        fields = [
            'id', 'theme', 'question_text', 'question_type', 'correct_answer', 'explanation',
            'difficulty', 'answer_synonyms','choices', 'accept_close_answer',
            'fake_answer_1', 'fake_answer_2', 'fake_answer_3'
        ]
        read_only_fields = ['id']


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'theme', 'question_text', 'question_type', 'correct_answer', 'accept_close_answer',
            'difficulty', 'fake_answer_1', 'fake_answer_2', 'fake_answer_3', 'explanation'
        ]
        read_only_fields = ['id']