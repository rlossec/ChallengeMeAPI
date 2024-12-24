from rest_framework.viewsets import ModelViewSet
from ..models import Theme
from ..serializers import ThemeSerializer

class ThemeViewSet(ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
