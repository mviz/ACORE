from django.contrib import admin
from surveys.models import SurveyQuestion, SurveyAnswer



class SurveyAdmin(admin.ModelAdmin):
    fields = ['question', 'integer_question']

admin.site.register(SurveyQuestion, SurveyAdmin)
admin.site.register(SurveyAnswer)