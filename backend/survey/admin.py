from django.contrib import admin
from .models import SpiritualGift, Question, SurveyResponse, Answer


@admin.register(SpiritualGift)
class SpiritualGiftAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['number', 'text', 'spiritual_gift']
    list_filter = ['spiritual_gift']
    search_fields = ['text', 'number']
    ordering = ['number']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ['question', 'rating']


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'created_at', 'completed_at']
    list_filter = ['created_at', 'completed_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'survey_response', 'question', 'rating']
    list_filter = ['rating', 'question__spiritual_gift']
    search_fields = ['survey_response__name']
