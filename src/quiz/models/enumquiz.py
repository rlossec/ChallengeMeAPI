
from django.contrib.auth import get_user_model
from django.db import models

from themes.models.theme import Theme
from .abstractquiz import AbstractQuiz


User = get_user_model()


class EnumQuiz(AbstractQuiz):
    text = models.TextField()
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enum_quizzes'
    )
    themes = models.ManyToManyField(
        Theme,
        related_name='enum_quizzes',
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.type:
            self.type = self.get_type()
        super().save(*args, **kwargs)

    def get_type(self):
        return "EN"


    def __str__(self):
        return self.text[:50]


class EnumAnswer(models.Model):
    quiz = models.ForeignKey(EnumQuiz, on_delete=models.CASCADE, related_name='enum_answers', null=True)
    answer_text_fr = models.CharField(max_length=255)
    answer_text_en = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.answer_text_fr
