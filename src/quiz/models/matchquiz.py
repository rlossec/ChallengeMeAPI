from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from . import Question
from .theme import Theme
from .abstractquiz import AbstractQuiz

User = get_user_model()


class MatchQuiz(AbstractQuiz):
    text = models.TextField()
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='match_quizzes'
    )
    themes = models.ManyToManyField(
        Theme,
        related_name='match_quizzes',
        blank=True
    )
    questions = models.ManyToManyField(Question, related_name='match_quizzes', blank=True)
    base_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.type:
            self.type = self.get_type()
        super().save(*args, **kwargs)

    def get_type(self):
        return "MT"

    def __str__(self):
        return self.title


class MatchPair(models.Model):
    match_quiz = models.ForeignKey(MatchQuiz, on_delete=models.CASCADE, related_name='pairs')
    text_clue = models.CharField(max_length=255, blank=True, null=True)
    picture_clue = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=255)

    def clean(self):
        if not self.text_clue and not self.picture_clue:
            raise ValidationError("Either text_clue or picture_clue must be provided.")

    def __str__(self):
        return self.answer
