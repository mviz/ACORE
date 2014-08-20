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

###                  The Global Variables           ###
counter = 0
line = []
stateOfNPCCounter = 0
nameList = ["Smith", "Johnson", "William", "Mary", "David", "Jennifer", "Chris", "Lisa", "Edward",
"Laura", "Sergio", "Sarah", "Emilie", "Matthew", "Kevin", "Liam",
"Ahmed", "Merriam"]
initialized = False
gameStatus = 'initial'
###                 End of Global Variables          ###


def makeNPC():
    global counter
    name = nameList.pop(randint(0, (len(nameList))-1))
    npc = human(name)
    npc.resourceVector = [1.0, 1.0, 1.0/(counter+1)]
    counter += 1
    return npc

def initialize(numInLine):
    global line
    count = 0
    for count in range(numInLine):
        line.append(makeNPC())
        count += 1 #TODO unless I'm missing something, isn't this redundant?

def displayLine():
    for person in line:
        print "\nName: " , person.name
        print "Emotion: " , person.getEmotion()
        print "Desired Action: " , person.nextAction
        #print "Protest Cost: " , round(person.protestCost(), 2)
        #print "Wait Cost: " , round(person.waitCost(), 2)
        #print "Pass Cost: " , round(person.passCost(), 2)
        #print "Resources: " , person.resourceVector
        #print "Weight Vector" , [round(Weight, 2) for Weight in person.resourceWeights]
        #print "New Resources: " , person.newResourceVector



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
    global stateOfNPCCounter, gameStatus, initialized, line
    #raw_input("\nNext Step?\n:")


    if initialized:
        if len(line) == 0:
            gameStatus = 'Over'
            print '\n ----------Game Over!------------ \n'
    else:
        initialize(numInLine = 6)  #The parameter tells the number of elements
        initialized = True

    context_data = {
        'npc_list':line,
        'npc_count':len(line),
    }

    response = HttpResponse()


    return render(request, 'surveys/home.html', context_data)

def reinitialize_data(request):
    # Resets the NPC data so that the model can be played more than once.  
    # Currently doesn't always work, for some unknown reason. TODO.
    global line, counter, nameList
    counter = 0 #yathi
    nameList = ["Smith", "Johnson", "William", "Mary", "David", "Jennifer", "Chris", "Lisa", "Edward", "Laura", "Sergio", "Sarah", "Emilie", "Matthew", "Kevin", "Liam", "Ahmed", "Merriam"]
    initialize(numInLine = 6) #TODO name list will eventually run out
    line_length = 6
    json_response = {
        "lineLength":line_length,
    } 
    return HttpResponse(json.dumps(json_response), content_type='application/json')


def initialize_data(request):
    global line, gameStatus
    npc_names = get_npc_names()
    npc_actions = get_npc_actions()
    npc_emotions = get_npc_emotions()
    npc_count = len(line)
    json_response = {
        'names':npc_names,
        'actions':npc_actions,
        'emotions':npc_emotions,
        "npc_count":npc_count,
        "gameStatus": convert_game_status(gameStatus),
    }
    return HttpResponse(json.dumps(json_response), content_type='application/json')


def acore_next_step(request):
    # Executes ACORE code.
    # Also returns important NPC information to be used in the javascript.
    global line, gameStatus

    passing_people = []
    ready_to_flip = False


    if gameStatus == 'initial':
        print 'Game status: ' , gameStatus
        for indx, person in enumerate(line):
            if indx != 0:
                person.newResourceVector = [person.resourceVector[0]-0.05, person.resourceVector[1]-0.4, line[indx-1].resourceVector[2]]
                print 'Action cost: ' , str(person.actionCost())
                if person.actionCost() > 0:
                    person.nextAction = 'Pass'
                    person.computeEmotion(0.95)

        displayLine()
        gameStatus = 'protest?'


    elif gameStatus == 'protest?':
        print 'Game status: ' , gameStatus
        for indx, person in enumerate(line):
            if indx < (len(line)-1):
                person.decideProtest(beingPassed = (line[indx+1].nextAction == "Pass"))

        for indx, person in enumerate(line):
            if indx < (len(line)-1):
                person.sanityCheck(indx, notbeingPassed = (line[indx+1].nextAction != 'Pass'))

        for indx, person in enumerate(line):
            if person.nextAction == 'Protest':
                person.newResourceVector = [person.resourceVector[0], person.resourceVector[1]-0.10, line[indx+1].resourceVector[2]]
                person.computeEmotion(0.95)


        displayLine()
        gameStatus = 'penultimate'

    elif gameStatus == 'penultimate':
        print 'The game status is ' , gameStatus
        for indx, person in enumerate(line):
            if indx != 0:
                if person.nextAction == 'Pass' and line[indx-1].nextAction == 'Protest':
                    if random() < 0.50:
                        print 'Being protested'
                        person.nextAction = 'Pass_Success'
                        person.computeEmotion(1)
                        line[indx-1].nextAction = 'Wait'
                        line[indx-1].newResourceVector = [line[indx-1].resourceVector[0], line[indx-1].resourceVector[1], line[indx].resourceVector[2]]
                        line[indx-1].computeEmotion(1)
                        person.resourceVector = person.newResourceVector
                        line[indx-1].resourceVector = line[indx-1].newResourceVector
                        line[indx], line[indx-1] = line[indx-1], line[indx] #Code to swap the 2 positions
                    else:
                        person.nextAction = 'Pass_Fail'
                        person.newResourceVector = [1, 0.5, person.resourceVector[2]]
                        person.computeEmotion(1)
                elif person.nextAction == 'Pass' and line[indx-1].nextAction == 'Wait':
                    if random() < 0.95:
                        print 'Not being protested'
                        person.nextAction = 'Pass_Success'
                        person.computeEmotion(1)
                        line[indx-1].newResourceVector = [line[indx-1].resourceVector[0], line[indx-1].resourceVector[1], line[indx-1].resourceVector[2]-0.3]
                        line[indx-1].computeEmotion(1)
                        line[indx-1].resourceVector = line[indx-1].newResourceVector
                        line[indx], line[indx-1] = line[indx-1], line[indx] #Code to swap the 2 positions
                    else:
                        person.nextAction = 'Pass_Fail'
                        person.newResourceVector = [1, 0.5, person.resourceVector[2]]
                        person.computeEmotion(1)

        for index, person in enumerate(line):
            if(person.getAction() == 'Pass_Success'):
                passing_people.append(index + 1) # +2 because they already made the pass, and the css is indexed from 1
        displayLine()
        gameStatus = 'final'

    elif gameStatus == 'final':
        print '\nThe game status is ' , gameStatus
        print str(line[0].name) , 'gets the Occulus Rift'
        line.pop(0)
        for indx, person in enumerate(line):
            person.nextAction = 'Wait'
            person.resourceVector[2] = 1.0/(indx+1)

        displayLine()
        gameStatus = 'initial'

    npc_names = get_npc_names()
    npc_actions = get_npc_actions()
    npc_emotions = get_npc_emotions()
    #npc_weights = get_npc_weights()
    #npc_resources = get_npc_resources()
    #npc_new_resources = get_npc_new_resources()
    npc_count = len(line)
    json_response = {
        'names':npc_names,
        'actions':npc_actions,
        'emotions':npc_emotions,
        #'weights':npc_weights,
        #'resources':npc_resources,
        #'newresources':npc_new_resources, 
        "npc_count":npc_count,
        "passing_list": passing_people,
        "gameStatus": convert_game_status(gameStatus),
    }

    return HttpResponse(json.dumps(json_response), content_type='application/json')

def convert_game_status(status):
    #Although not a necessary function, it's used for clarity in the javacsript side, because the
    #game status will change to the subsequent status before the data is sent through JSON.
    if(status == 'protest?'):
        return 'initial'
    elif(status == 'penultimate'):
        return 'protest?'
    elif(status=='final'):
        return 'penultimate'
    else:
        return 'final'

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



