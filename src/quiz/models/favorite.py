
from django.contrib.auth import get_user_model
from django.db import models

from .theme import Theme

User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'theme')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user} a ajouté {self.theme}"
