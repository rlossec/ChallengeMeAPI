
import random

from django.db import models

from .theme import Theme
from .synonym import Synonym


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('TXT', 'Texte'),
        ('IMG', 'Image'),
        ('CHO', 'Choices')
    ]

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    question_text = models.TextField()
    image = models.ImageField('Image', upload_to="question_images/", blank=True, null=True)
    correct_answer = models.CharField(max_length=255)
    accept_close_answer = models.BooleanField(default=False, blank=False, null=False)
    difficulty = models.FloatField(default=0.0)
    valid = models.BooleanField(default=False, blank=False, null=False)
    fake_answer_1 = models.CharField(max_length=255, blank=True, null=True)
    fake_answer_2 = models.CharField(max_length=255, blank=True, null=True)
    fake_answer_3 = models.CharField(max_length=255, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def answer_synonyms(self):
        synonyms = Synonym.objects.filter(reference_answer=self.correct_answer)
        return [syn.synonym_text for syn in synonyms]

    @property
    def choices(self):
        answers = [self.correct_answer]
        if self.fake_answer_1:
            answers.append(self.fake_answer_1)
        if self.fake_answer_2:
            answers.append(self.fake_answer_2)
        if self.fake_answer_3:
            answers.append(self.fake_answer_3)
        random.shuffle(answers)
        return answers

    def __str__(self):
        return self.question_text[:50]
