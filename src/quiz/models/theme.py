
from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_theme = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subthemes')
    image = models.ImageField(upload_to="theme_images/", blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
