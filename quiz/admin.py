from django.contrib import admin
from .models import User, Question, Answer, Survey

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]

admin.site.register(User)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Survey)


