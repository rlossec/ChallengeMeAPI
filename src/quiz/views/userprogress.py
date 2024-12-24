from rest_framework.viewsets import ModelViewSet
from ..models import UserProgress
from ..serializers import UserProgressSerializer

class UserProgressViewSet(ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
