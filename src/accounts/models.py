from pathlib import Path

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Supprimer l'ancienne image si un nouvel avatar est fourni
        if self.pk:
            old_avatar = User.objects.filter(pk=self.pk).values_list('avatar', flat=True).first()
            if old_avatar and self.avatar and old_avatar != self.avatar.name:
                old_avatar_path = Path(self.avatar.storage.location) / old_avatar
                if old_avatar_path.exists():
                    old_avatar_path.unlink()
        super().save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=User)
def delete_avatar_on_user_delete(sender, instance, **kwargs):
    """Supprime l'avatar associé lorsqu'un utilisateur est supprimé."""
    if instance.avatar:
        avatar_path = Path(instance.avatar.path)
        if avatar_path.exists():
            avatar_path.unlink()
