from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ThemeViewSet, QuestionViewSet, FavoriteListView, AddFavoriteView, RemoveFavoriteView

router = DefaultRouter()
router.register('themes', ThemeViewSet, basename='theme')
router.register('questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('themes/favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('themes/<int:theme_id>/favorites/add/', AddFavoriteView.as_view(), name='add-favorite'),
    path('themes/<int:theme_id>/favorites/remove/', RemoveFavoriteView.as_view(), name='remove-favorite'),
] + router.urls
