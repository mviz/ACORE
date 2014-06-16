from django import forms
from . import models

class SurveyForm(forms.Form):
    answer = forms.CharField(max_length=255)