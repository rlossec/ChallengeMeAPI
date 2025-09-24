from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from themes.serializers.themes import ReorderSubthemesSerializer

from ..models import Theme
from ..serializers import ThemeDetailedSerializer


class ThemeViewSet(ModelViewSet):
    queryset = Theme.objects.filter(parent_theme__isnull=True).order_by('order')
    serializer_class = ThemeDetailedSerializer

    def get_queryset(self):
        """
        - Pour la liste, on récupère uniquement les thèmes de premier niveau.
        - Pour les autres actions (RUD), on récupère tous les thèmes.
        """
        if self.action == 'list':
            return Theme.objects.filter(parent_theme__isnull=True).order_by('order')
        return Theme.objects.all()

    # Méthode pour obtenir tous les sous-thèmes récursivement
    def get_all_subthemes(self, theme):
        subthemes = Theme.objects.filter(parent_theme=theme)
        all_subthemes = list(subthemes)
        for subtheme in subthemes:
            all_subthemes.extend(self.get_all_subthemes(subtheme))
        return all_subthemes

    @action(detail=True, methods=['post'])
    def reorder_subthemes(self, request, pk=None):
        """
        Endpoint pour réordonner les sous-thèmes d'un thème donné.
        """

        theme = self.get_object()
        serializer = ReorderSubthemesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subtheme_ids = serializer.validated_data['subtheme_order']

        # Vérifie que tous les IDs appartiennent aux sous-thèmes du thème actuel
        if not all(
            theme.subthemes.filter(id=subtheme_id).exists()
            for subtheme_id in subtheme_ids
        ):
            return Response(
                {"error": "Certains sous-thèmes ne correspondent pas à ce thème parent."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Met à jour l'ordre de chaque sous-thème
        for index, subtheme_id in enumerate(subtheme_ids):
            subtheme = Theme.objects.get(id=subtheme_id)
            subtheme.order = index
            subtheme.save()

        return Response(
            {"message": "L'ordre des sous-thèmes a été mis à jour avec succès."},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'], url_path='questions')
    def theme_questions(self, request, pk=None):
        """
        Endpoint pour récupérer toutes les questions d'un thème donné
        et de ses sous-thèmes récursivement.
        """
        theme = self.get_object()

        # Obtenir tous les sous-thèmes récursivement
        all_subthemes = self.get_all_subthemes(theme)

        # Récupérer les questions associées au thème principal et aux sous-thèmes
        themes_to_include = [theme] + all_subthemes
        questions = Question.objects.filter(theme__in=themes_to_include)

        serializer = QuestionPlaySerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
