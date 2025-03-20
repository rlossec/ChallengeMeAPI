
from django.contrib.auth import get_user_model
from django.db import models

from quiz.models import Theme
from quiz.models.abstractquiz import AbstractQuiz

User = get_user_model()


class ClassicQuiz(AbstractQuiz):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='classic_quizzes'
    )
    themes = models.ManyToManyField(
        Theme,
        related_name='classic_quizzes',
        blank=True
    )
    questions = models.ManyToManyField('Question', related_name='classic_quizzes')

    def save(self, *args, **kwargs):
        if not self.type:
            self.type = self.get_type()
        super().save(*args, **kwargs)

    def get_type(self):
        return "CL"

    def __str__(self):
        return self.title
