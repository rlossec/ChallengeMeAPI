from django.contrib.auth import get_user_model
from django.db import models
import random

User = get_user_model()

class Theme(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    parent_theme = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subthemes')
    icon = models.CharField(max_length=50, blank=True, null=True)  # Pour stocker des icônes comme 🔵

    def __str__(self):
        return self.name

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('text', 'Réponse ouverte'),
        ('multiple_choice', 'Choix multiple'),
    ]

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField(blank=True, null=True)
    difficulty = models.FloatField(default=0.0)
    fake_answer_1 = models.CharField(max_length=255, blank=True, null=True)
    fake_answer_2 = models.CharField(max_length=255, blank=True, null=True)
    fake_answer_3 = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    attempts = models.PositiveIntegerField(default=0)
    correct_attempts = models.PositiveIntegerField(default=0)
    last_attempted = models.DateTimeField(auto_now=True)

    def success_rate(self):
        if self.attempts == 0:
            return 0
        return (self.correct_attempts / self.attempts) * 100

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text[:30]} - {self.success_rate()}%"


class Synonym(models.Model):
    synonym_text = models.TextField()
    reference_answer = models.TextField()

    def __str__(self):
        return self.synonym_text
