from django.shortcuts import get_object_or_404, render
from django.views import generic
from surveys.models import Question, Answer
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from . import forms

import pdb
import random
import json

#TODO_yathi, this dummy class needs to be replaced eventually
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


class Results(generic.ListView):
    template_name = 'surveys/survey_results.html'
    model = Question

    def get_context_data(self, **kwargs):
        return super(Results, self).get_context_data(**kwargs)

class SurveyList(generic.ListView):
    model = Question
    template_name = "surveys/survey_list.html"

    def get_context_data(self, **kwargs): 
        return super(SurveyList, self).get_context_data(**kwargs)

def submit_survey(request):
    choices = []
    temp = []
    for key, value in request.POST.iteritems():
        #pdb.set_trace()
        if(value == "7qoErK6uBY3yjCZO7YA7VeHlGiDlN5qs"):
            continue
        if(key=="csrfmiddlewaretoken"):
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

    return HttpResponseRedirect('/surveys/results') 


def homepage_view(request):
    #ajax for updating images
    if(request.is_ajax()):
        if(random.randint(0,1)):
            image =  'http://theumbrellaagency.com/wp-content/uploads/2009/07/umbrella_agency_smiley_face-200x200.jpg'
        else:
            image =  'http://twilight.ponychan.net/chan/arch/src/130751482204.png'

        json_response = {'npc_data':{'npc_image':image}}
        return HttpResponse(json.dumps(json_response), content_type='application/json')

    #TODO_yathi these NPCs will be replaced by your NPC list. It goes into the context dictionary so that the template can access it
    npc_list = [ Npc_temp('Mary', 'joy', 'nothing'), Npc_temp('Jane', 'hope', 'skip'), Npc_temp('Emma', 'distress', 'attack'), Npc_temp('Stone', 'sorrow', 'cry'), Npc_temp('Toby', 'joy','nothing')]
    #TODO_yathi, npc_count just needs to be the number of npcs
    npc_count = 5
    context_data = {
        'npc_list':npc_list,
        'npc_count':npc_count,
    }

    return render(request, 'surveys/home.html', context_data)



