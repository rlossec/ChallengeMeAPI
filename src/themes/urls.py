from django.urls import path, include
from rest_framework.routers import DefaultRouter

from themes.views.favorites import FavoriteListView, AddFavoriteView, RemoveFavoriteView
from themes.views.themes import ThemeViewSet


router = DefaultRouter()
router.register('themes', ThemeViewSet, basename='theme')

urlpatterns = [
    path('themes/favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('themes/<int:theme_id>/favorites/add/', AddFavoriteView.as_view(), name='add-favorite'),
    path('themes/<int:theme_id>/favorites/remove/', RemoveFavoriteView.as_view(), name='remove-favorite'),
] + router.urls
