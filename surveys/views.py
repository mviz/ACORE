from django.shortcuts import get_object_or_404
from django.views import generic
from surveys.models import Question, Answer
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from . import forms

import pdb

class Results(generic.ListView):
    template_name = 'surveys/survey_results.html'
    model = Question

    def get_context_data(self, **kwargs):
        return super(Results, self).get_context_data(**kwargs)

class SurveyList(generic.ListView):
    model = Question
    template_name = "surveys/survey_list.html"
    #form_class = forms.SurveyForm

    def get_context_data(self, **kwargs): 
        return super(SurveyList, self).get_context_data(**kwargs)

def submit_survey(request):
    choices = []
    temp = []
    for key, value in request.POST.iteritems():
        #choices.append((key,value))
        if(value == "7qoErK6uBY3yjCZO7YA7VeHlGiDlN5qs"):
            continue
        temp.append(value)

        try:
            choices.append(get_object_or_404(Answer, pk=value))
        except(KeyError, Answer.DoesotExist):
            return render(request, 'surveys/questions.html', 
            { 'not_complete':"Please answer all questions",})

    for answer_obj in choices:
        answer_obj.votes += 1
        answer_obj.save()

    #pdb.set_trace()

    return HttpResponseRedirect('http://127.0.0.1:8000/surveys/results/')

    


