from django.contrib import admin
from surveys.models import Question, Answer



class SurveyAdmin(admin.ModelAdmin):
    fields = ['question', 'integer_question']

admin.site.register(Question, SurveyAdmin)
admin.site.register(Answer)