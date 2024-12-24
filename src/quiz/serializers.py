from rest_framework import serializers
from .models import Theme, Question, UserProgress, Synonym

class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        fields = ['synonym_text', 'reference_answer']

class QuestionSerializer(serializers.ModelSerializer):
    answer_synonyms = serializers.ReadOnlyField()
    choices = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = [
            'theme', 'question_text', 'question_type', 'correct_answer', 'explanation',
            'difficulty', 'answer_synonyms', 'choices'
        ]

class ThemeSerializer(serializers.ModelSerializer):
    subthemes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ['name', 'description', 'parent_theme', 'icon', 'subthemes']

class UserProgressSerializer(serializers.ModelSerializer):
    success_rate = serializers.ReadOnlyField()

    class Meta:
        model = UserProgress
        fields = ['user', 'question', 'attempts', 'correct_attempts', 'last_attempted', 'success_rate']
