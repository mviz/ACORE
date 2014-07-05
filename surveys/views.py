from django.shortcuts import get_object_or_404, render
from django.views import generic
from surveys.models import Question, Answer
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from . import forms

import pdb


class Npc_temp:
    name = ''
    emotion = ''
    action = ''
    def __init__(self, name, emotion, action):
        self.name = name
        self.emotion = emotion
        self.action = action

    def get_name(self):
        return self.name
    def get_emotion(self):
        return self.emotion
    def get_action(self):
        return self.action

def homepage_view(request):
    npc_list = [ Npc_temp('Mary', 'joy', 'nothing'), Npc_temp('Jane', 'hope', 'skip'), Npc_temp('Emma', 'distress', 'attack'), Npc_temp('Stone', 'sorrow', 'cry'), Npc_temp('Toby', 'joy','nothing')]
    context_data = {
        'npc_list':npc_list,
    }
    return render(request, 'surveys/home.html', context_data)






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
        pdb.set_trace()
        if(value == "7qoErK6uBY3yjCZO7YA7VeHlGiDlN5qs"):
            continue
        temp.append(value)

        try:
            choices.append(get_object_or_404(Answer, pk=value))
        except(KeyError, Answer.DoesNotExist):
            return render(request, 'surveys/questions.html', 
            { 'not_complete':"Please answer all questions",})

    for answer_obj in choices:
        answer_obj.votes += 1
        answer_obj.save()

    #pdb.set_trace()

    return HttpResponseRedirect('http://acore-survey.herokuapp.com/surveys/results/') # TODO THIS URL WAS POINTED TO A WRONG ABSOLUTE ADDRESS FIX IT NAO

    


