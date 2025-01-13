from rest_framework import serializers

from quiz.models import Theme


class ThemeSerializer(serializers.ModelSerializer):
    subthemes = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ['id', 'name', 'description', 'parent_theme', 'color', 'order', 'subthemes']

    def get_subthemes(self, obj):
        """
        Récupère les sous-thèmes avec tous leurs détails, y compris leurs sous-sous-thèmes.
        """
        subthemes = obj.subthemes.order_by('order')
        return ThemeSerializer(subthemes, many=True).data


class ReorderSubthemesSerializer(serializers.Serializer):
    subtheme_order = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
