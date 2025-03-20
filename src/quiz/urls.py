from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ThemeViewSet, QuestionViewSet, FavoriteListView, AddFavoriteView, RemoveFavoriteView
from .views import ClassicQuizViewSet, EnumQuizViewSet, MatchQuizViewSet, AllQuizViewSet


router = DefaultRouter()
router.register('themes', ThemeViewSet, basename='theme')
router.register('questions', QuestionViewSet, basename='question')
router.register(r'quiz/classic', ClassicQuizViewSet)
router.register(r'quiz/enum', EnumQuizViewSet)
router.register(r'quiz/match', MatchQuizViewSet)


urlpatterns = [
    path('themes/favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('themes/<int:theme_id>/favorites/add/', AddFavoriteView.as_view(), name='add-favorite'),
    path('themes/<int:theme_id>/favorites/remove/', RemoveFavoriteView.as_view(), name='remove-favorite'),

    path('quiz/', AllQuizViewSet.as_view({'get': 'list', 'post': 'create'})),

] + router.urls
