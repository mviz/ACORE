from django.shortcuts import get_object_or_404, render
from django.views import generic
from surveys.models import Question, Answer
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from . import forms

import pdb
import json

from emotion import *
from npc import human
import time
from random import random, randint

counter = 0
line = []
stateOfNPCCounter = 0
nameList = ["Smith", "Johnson", "William", "Mary", "David", "Jennifer", "Chris", "Lisa", "Edward",
"Laura", "Sergio", "Sarah", "Emilie", "Matthew", "Kevin", "Liam",
"Ahmed", "Merriam"]
initialized = False

def makeNPC():
    global counter
    name = nameList.pop(randint(0, (len(nameList))-1))
    npc = human(name)
    npc.resourceVector[2] += counter*0.3
    counter += 1
    return npc

def initialize():
    global line
    count = 0
    for count in range(6):
        line.append(makeNPC())
        count += 1

def displayLine():
    for person in line:
        print "\nName: " , person.name
        print "Emotion: " , person.emotion
        print "Desired Action: " , person.bestAction()
        print "Protest Cost: " , person.protestCost()
        print "Wait Cost: " , person.waitCost()
        print "Pass Cost: " , person.passCost()
        print "Resources: " , person.resourceVector
        print "New Resources: " , person.newResourceVector



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
    global line
    choices = []
    temp = []

    context_data = {
        'npc_list':line,
        'npc_count':len(line),
    }


    for key, value in request.POST.iteritems():
        if(key=="csrfmiddlewaretoken"):
            continue
        temp.append(value)

        try:
            choices.append(get_object_or_404(Answer, pk=value))
        except(KeyError, Answer.DoesNotExist):
            context_data['not_complete'] = 'Please answer all of the questions'
            return render(request, 'surveys/questions.html', context_data)

    #Restrict users to a single submission
    #TODO
    if (request.COOKIES.has_key('submitted')):
        pdb.set_trace()
        context_data['not_complete'] = 'You can only submit once.'
        return render(request, 'surveys/questions.html', context_data)

    else:
        pdb.set_trace()
        response = HttpResponse('Submission_Cookie')
        response.set_cookie('submitted', 'yes')

    for answer_obj in choices:
        answer_obj.votes += 1
        answer_obj.save()
    return HttpResponseRedirect('/surveys/results') 


def homepage_view(request):
    global initialized
    global line

    if not initialized:
        initialize()
        initialized = True

    context_data = {
        'npc_list':line,
        'npc_count':npc_count,
    }

    response = HttpResponse()

    npc_count = len(line)

    return render(request, 'surveys/home.html', context_data)


def ajax_view_handler(request):
    global line
    global stateOfNPCCounter

    passing_people = []
    ready_to_flip = False

    stateOfNPCCounter += 1

    if (stateOfNPCCounter%3)!=0:
        for indx, person in enumerate(line):
            print "\nName: " , person.name, " " , str(indx)

            if person.bestAction() == "Pass":
                line[indx-1].beingPassed = True
            if person.bestAction() == "Protest":
                #print "\nIndex is ", str(indx), "And the len is : ", str(len(line)), "\n"
                if indx < (len(line)-1):
                    line[indx+1].beingProtested == True
    elif (stateOfNPCCounter%3)==0:
        for indx, person in enumerate(line):
            if person.finalAction():
                passing_people.append(indx)

        print "The people passing :" , passing_people
        for indx in passing_people:
            if indx != 0:
                line[indx], line[indx-1] = line[indx-1], line[indx]

        for person in line:
            if person.nextAction == "Protest":
                person.nextAction = "Wait"

        ready_to_flip = True


    npc_names = get_npc_names()
    npc_actions = get_npc_actions()
    npc_emotions = get_npc_emotions()
    npc_weights = get_npc_weights()
    npc_resources = get_npc_resources()
    npc_new_resources = get_npc_new_resources()
    npc_count = len(line)
    json_response = {
        'names':npc_names,
        'actions':npc_actions,
        'emotions':npc_emotions,
        'weights':npc_weights,
        'resources':npc_resources,
        'newresources':npc_new_resources, 
        "npc_count":npc_count,
        "passing_list": passing_people,
        "finalAction": ready_to_flip,
    }
    return HttpResponse(json.dumps(json_response), content_type='application/json')

# TODO figure out how to pass a method from another file & inside a class to a function
def get_npc_names():
    global line
    new_list = []
    for npc in line:
        new_list.append(npc.sayHello())
    return new_list

def get_npc_actions():
    global line
    new_list = []
    for npc in line:
        new_list.append(npc.getAction())
    return new_list

def get_npc_emotions():
    global line
    new_list = []
    for npc in line:
        new_list.append(npc.getEmotion())
    return new_list

def get_npc_weights():
    global line
    new_list = []
    for npc in line:
        new_list.append(npc.getWeights())
    return new_list

def get_npc_resources():
    global line
    new_list = []
    for npc in line:
        temp = []
        for res in npc.getResources():
            temp.append(((1000*res)//1)/1000)
        new_list.append(temp)
    return new_list

def get_npc_new_resources():
    global line
    new_list = []
    for npc in line:
        temp = []
        for nres in npc.getNewResources():
            temp.append(((1000*nres)//1)/1000)
        new_list.append(temp)
    return new_list



