
from rest_framework import serializers
from quiz.models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    theme_id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ['user', 'theme_id', 'added_at']
        read_only_fields = ['user', 'added_at']

    def validate_theme_id(self, value):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, theme_id=value).exists():
            raise serializers.ValidationError("This theme id already in your favorites.")
        return value
