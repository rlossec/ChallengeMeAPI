from django.contrib import admin

from quiz.models import ClassicQuiz, EnumQuiz, EnumAnswer, MatchQuiz, MatchPair



class QuestionInline(admin.TabularInline):
    model = ClassicQuiz.questions.through
    extra = 1


@admin.register(ClassicQuiz)
class ClassicQuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator')
    search_fields = ('title', 'creator__username')
    list_filter = ('themes',)
    inlines = [QuestionInline]
    exclude = ('questions',)


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
