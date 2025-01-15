
from django.db import models

class Synonym(models.Model):
    synonym_text = models.TextField()
    reference_answer = models.TextField()

    def __str__(self):
        return self.synonym_text