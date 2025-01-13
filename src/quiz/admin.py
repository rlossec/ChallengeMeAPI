from django.contrib import admin

from quiz.models import Question, Theme, Synonym, Favorite

admin.site.register(Theme)
admin.site.register(Favorite)

admin.site.register(Question)
admin.site.register(Synonym)


