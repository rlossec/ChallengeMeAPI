
from rest_framework import serializers

from quiz.models import Synonym


class SynonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synonym
        fields = ['synonym_text', 'reference_answer']


