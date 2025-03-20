from django.contrib import admin
from django import forms
from django.forms import BaseInlineFormSet

from quiz.models import Question, Theme, Synonym, Favorite, ClassicQuiz, EnumQuiz, EnumAnswer, MatchQuiz, MatchPair

admin.site.register(Theme)
admin.site.register(Favorite)
admin.site.register(Synonym)


class QuestionInline(admin.TabularInline):
    model = ClassicQuiz.questions.through
    extra = 1


@admin.register(ClassicQuiz)
class ClassicQuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator')  # Colonnes affichées dans la liste
    search_fields = ('title', 'creator__username')  # Recherche par titre ou créateur
    list_filter = ('themes',)  # Filtrage par thèmes
    inlines = [QuestionInline]  # Ajout des questions en tant qu'inline
    exclude = ('questions',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']  # Recherche par texte de la question
    list_display = ['question_text', 'theme', 'difficulty', 'valid']
    list_filter = ['theme', 'valid', 'difficulty']  # Filtrer par thème, validation, difficulté


class EnumAnswerInline(admin.TabularInline):
    model = EnumAnswer
    extra = 1

@admin.register(EnumQuiz)
class EnumQuizAdmin(admin.ModelAdmin):
    list_display = ('text', 'valid', 'difficulty')
    search_fields = ('text',)
    inlines = [EnumAnswerInline]


class MatchPairInline(admin.TabularInline):
    model = MatchPair


@admin.register(MatchQuiz)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('text', 'valid', 'difficulty')
    inlines = [MatchPairInline]
