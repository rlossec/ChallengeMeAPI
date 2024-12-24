from django.contrib import admin

from quiz.models import Question, Theme, UserProgress, Synonym

admin.site.register(Theme)
admin.site.register(Question)
admin.site.register(UserProgress)
admin.site.register(Synonym)
