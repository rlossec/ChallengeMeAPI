from django.urls import path

from rest_framework.routers import DefaultRouter


from .views import ClassicQuizViewSet, EnumQuizViewSet, MatchQuizViewSet, AllQuizViewSet


router = DefaultRouter()

router.register(r'quiz/classic', ClassicQuizViewSet)
router.register(r'quiz/enum', EnumQuizViewSet)
router.register(r'quiz/match', MatchQuizViewSet)


urlpatterns = [

    path('quiz/', AllQuizViewSet.as_view({'get': 'list', 'post': 'create'})),

] + router.urls
