from django.contrib import admin
from .models import Badge, Evaluation, Question, Choice, UserResult

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'evaluation', 'order')
    list_filter = ('evaluation',)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class EvaluationAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'skill', 'passing_score', 'is_active')
    list_filter = ('skill', 'is_active')

admin.site.register(Badge)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserResult)
