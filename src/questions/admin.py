from django.contrib import admin

from .models import Question, Synonym

# Register your models here.
admin.site.register(Synonym)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    list_display = ['question_text', 'theme', 'difficulty', 'valid']
    list_filter = ['theme', 'valid', 'difficulty']
