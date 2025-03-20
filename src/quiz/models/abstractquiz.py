import uuid

from django.db import models
from django.contrib.auth import get_user_model

from .theme import Theme

User = get_user_model()


class AbstractQuiz(models.Model):
    QUIZ_TYPE_CHOICES = {
        "CL": "Classic",
        "RA": "Random",
        "EN": "Enumeration",
        "MT": "Match"
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=2, choices=QUIZ_TYPE_CHOICES, default="CL")
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    themes = models.ManyToManyField(Theme, related_name='quizzes', blank=True)
    difficulty = models.FloatField(default=0.0)
    valid = models.BooleanField(default=False, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True