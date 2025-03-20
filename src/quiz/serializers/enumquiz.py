
from rest_framework import serializers
from quiz.models import EnumQuiz, EnumAnswer


class EnumAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumAnswer
        fields = ["answer_text_fr",  "answer_text_en", "order"]


class EnumQuizSerializer(serializers.ModelSerializer):
    enum_answers = EnumAnswerSerializer(many=True)

    class Meta:
        model = EnumQuiz
        fields = ['id', 'title', 'text', 'type', 'difficulty', 'creator', 'themes', 'enum_answers']
        read_only_fields = ['id', 'type', 'creator']

    def update(self, instance, validated_data):
        # Extraire les données pour themes et enum_answers
        themes_data = validated_data.pop('themes', None)
        enum_answers_data = validated_data.pop('enum_answers', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if themes_data is not None:
            instance.themes.set(themes_data)

        # Mettre à jour les réponses existantes ou en créer de nouvelles
        existing_answers = {answer.id: answer for answer in instance.enum_answers.all()}
        for answer_data in enum_answers_data:
            answer_id = answer_data.get('id', None)
            if answer_id and answer_id in existing_answers:
                # Mettre à jour une réponse existante
                answer = existing_answers.pop(answer_id)
                for attr, value in answer_data.items():
                    setattr(answer, attr, value)
                answer.save()
            else:
                # Créer une nouvelle réponse
                EnumAnswer.objects.create(quiz=instance, **answer_data)

        # Supprimer les réponses restantes non incluses dans la requête
        for answer in existing_answers.values():
            answer.delete()

        return instance