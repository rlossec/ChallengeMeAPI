from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from quiz.models import Theme, Favorite
from quiz.serializers import ThemeDetailedSerializer


class FavoriteListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Récupère les thèmes favoris de l'utilisateur connecté
        favorites = Favorite.objects.filter(user=request.user)
        serializer = ThemeDetailedSerializer([favorite.theme for favorite in favorites], many=True)
        return Response(serializer.data)

class AddFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, theme_id):
        try:
            theme = Theme.objects.get(id=theme_id)
        except Theme.DoesNotExist:
            return Response({"detail": "Theme not found."}, status=status.HTTP_404_NOT_FOUND)

        # Vérifie si le thème est déjà dans les favoris
        if Favorite.objects.filter(user=request.user, theme=theme).exists():
            return Response({"detail": "Theme already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        # Ajoute le thème aux favoris
        Favorite.objects.create(user=request.user, theme=theme)
        return Response({"detail": "Theme added to favorites."}, status=status.HTTP_201_CREATED)


class RemoveFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, theme_id):
        try:
            theme = Theme.objects.get(id=theme_id)
        except Theme.DoesNotExist:
            return Response({"detail": "Theme not found."}, status=status.HTTP_404_NOT_FOUND)

        # Supprime le thème des favoris
        favorite = Favorite.objects.filter(user=request.user, theme=theme).first()
        if not favorite:
            return Response({"detail": "Theme not in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        favorite.delete()
        return Response({"detail": "Theme removed from favorites."}, status=status.HTTP_200_OK)
