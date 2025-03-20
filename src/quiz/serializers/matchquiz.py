
from rest_framework import serializers
from quiz.models import MatchQuiz, MatchPair


class MatchPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchPair
        fields = []  # Aucun champ direct, on personnalise la représentation

    def to_representation(self, instance):
        # Récupère la base_url depuis le quiz lié
        base_url = instance.match_quiz.base_url

        # Détermine la clé (texte ou image)
        key = instance.text_clue if instance.text_clue else instance.picture_clue

        # Ajoute la base_url si c'est une image et si base_url est défini
        if instance.picture_clue and base_url:
            key = f"{base_url.rstrip('/')}/{instance.picture_clue.lstrip('/')}"

        # Retourne la paire clé-valeur
        return {key: instance.answer}


class MatchQuizSerializer(serializers.ModelSerializer):
    pairs = MatchPairSerializer(many=True, read_only=True)

    class Meta:
        model = MatchQuiz
        fields = ["id", "title", "text", 'type', "difficulty", "themes", "pairs"]

    def validate_pairs(self, value):
        print("PAIRS DATA:", value)  # Debugging
        return value


class MatchPairCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchPair
        fields = ["id", "text_clue", "picture_clue", "answer", "match_quiz"]
        read_only_fields = ["match_quiz"]


class MatchQuizCRUDSerializer(serializers.ModelSerializer):
    pairs = MatchPairCRUDSerializer(many=True)

    class Meta:
        model = MatchQuiz
        fields = ["id", "title", "text", "type", "difficulty", "themes", "base_url", "pairs"]

    def create(self, validated_data):
        # Extraire les données des thèmes et des paires

        themes_data = validated_data.pop('themes', [])
        pairs_data = validated_data.pop('pairs', [])

        user = self.context['request'].user
        match_quiz = MatchQuiz.objects.create(creator=user, **validated_data)

        # Associer les thèmes
        match_quiz.themes.set(themes_data)

        # Créer les paires associées
        for pair_data in pairs_data:
            MatchPair.objects.create(match_quiz=match_quiz, **pair_data)
        return match_quiz

    def update(self, instance, validated_data):
        # Extraire les données des thèmes et des paires
        themes_data = validated_data.pop('themes', [])
        pairs_data = validated_data.pop('pairs', [])
        # Mettre à jour les champs simples du MatchQuiz
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour les thèmes associés
        if themes_data:
            instance.themes.set(themes_data)

        # Récupérer les paires existantes sous forme de triplets avec leurs instances
        existing_pairs = {
            (pair.text_clue, pair.picture_clue, pair.answer): pair for pair in instance.pairs.all()
        }

        # Construire un ensemble des triplets soumis dans la requête
        sent_triplets = set()
        for pair_data in pairs_data:
            triplet = (pair_data.get("text_clue"), pair_data.get("picture_clue"), pair_data.get("answer"))
            sent_triplets.add(triplet)

            # Si le triplet n'existe pas, on ajoute la nouvelle paire
            if triplet not in existing_pairs:
                MatchPair.objects.create(match_quiz=instance, **pair_data)

        # Supprimer les paires qui ne figurent pas dans la requête
        for triplet, pair_instance in existing_pairs.items():
            if triplet not in sent_triplets:
                pair_instance.delete()

        return instance

