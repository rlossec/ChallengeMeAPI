from rest_framework import serializers

from quiz.models import Theme


class ThemeDetailedSerializer(serializers.ModelSerializer):
    subthemes = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ['id', 'name', 'description', 'parent_theme', 'color', 'order', 'subthemes']

    def get_subthemes(self, obj):
        subthemes = obj.subthemes.order_by('order')
        return ThemeDetailedSerializer(subthemes, many=True).data


class ThemeSerializer(serializers.ModelSerializer):
    subthemes = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ['id', 'name', 'description', 'parent_theme', 'color', 'order', 'subthemes']

    def get_subthemes(self, obj):
        subthemes = obj.subthemes.order_by('order')
        return [subtheme.name for subtheme in subthemes]


class ReorderSubthemesSerializer(serializers.Serializer):
    subtheme_order = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )
