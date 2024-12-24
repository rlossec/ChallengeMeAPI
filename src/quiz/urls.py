from rest_framework.routers import DefaultRouter
from .views import ThemeViewSet, QuestionViewSet, UserProgressViewSet

router = DefaultRouter()
router.register('themes', ThemeViewSet, basename='theme')
router.register('questions', QuestionViewSet, basename='question')
router.register('user-progress', UserProgressViewSet, basename='userprogress')

urlpatterns = router.urls
