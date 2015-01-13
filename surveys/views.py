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
import itertools
from random import random, randint

###                  The Global Variables           ###
line = []
stateOfNPCCounter = 0
#nameList = ["Alex", "Smith", "Johnson", "William", "Mary", "David", "Jennifer", "Chris", "Lisa", "Edward",
#"Laura", "Sergio", "Sarah", "Emilie", "Matthew", "Kevin", "Liam",
#"Ahmed", "Merriam"]
nameList = ["Alex", "Smith", "Jonathan", "William", "David",  "Chris", "Edward",
"Sergio", "Matthew", "Kevin", "Liam", "Ahmed"]
initialized = False
gameStatus = 'initial'
###                 End of Global Variables          ###

def reverse_enumerate(iterable):
    """
    Enumerate over an iterable in reverse order while retaining proper indexes
    """
    return itertools.izip(reversed(xrange(len(iterable))), reversed(iterable))

def makeNPC(position):
    name = nameList.pop(randint(0, (len(nameList))-1))
    npc = human(name)
    npc.resourceVector = [1.0, 1.0, 1.0/(position+1)]
    return npc

def initialize(numInLine):
    global line
    count = 0
    for count in range(numInLine):
        line.append(makeNPC(count))
        
def displayLine():
    #A DEBUG function used to check the values. 
    for person in line:
        print "\nName: " , person.name
        print "Emotion: " , person.getEmotion()
        print "Desired Action: " , person.nextAction
        print "Resources: " , person.resourceVector
        #print "Weight Vector" , [round(Weight, 2) for Weight in person.resourceWeights]
        #print "New Resources: " , person.newResourceVector



class Results(generic.ListView):
    template_name = 'surveys/survey_results.html'
    model = Question

    def get_context_data(self, **kwargs):
        return super(Results, self).get_context_data(**kwargs)

class SurveyList(generic.ListView):
    model = Question
    template_name = "surveys/survey_google.html"

    def get_context_data(self, **kwargs):
        return super(SurveyList, self).get_context_data(**kwargs)

def acoreInfoPopup(request):
    return render(request, 'surveys/infoPopup.html')

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

    return render(request, 'surveys/home.html', context_data)

def reinitialize_data(request):
    # Resets the NPC data so that the model can be played more than once.
    # Currently doesn't always work, for some unknown reason. TODO.
    global line, counter, nameList
    if(len(line) == 0):
        counter = 0 #yathi
        nameList = ["Smith", "Johnson", "William", "Mary", "David", "Jennifer", "Chris",
         "Lisa", "Edward", "Laura", "Sergio", "Sarah", "Emilie", "Matthew", "Kevin", "Liam", "Ahmed", "Merriam"]
        initialize(numInLine = 6) #TODO name list will eventually run out

    json_response = {
        "lineLength":len(line),
    }
    return HttpResponse(json.dumps(json_response), content_type='application/json')


def initialize_data(request):
    global line, gameStatus
    npc_names = get_npc_names()
    npc_actions = get_npc_actions()
    npc_emotions = get_npc_emotions()
    npc_health = get_npc_health()
    npc_count = len(line)
    json_response = {
        'names':npc_names,
        'actions':npc_actions,
        'emotions':npc_emotions,
        'health':npc_health,
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
            person.halveEmotion()
            if indx != 0:
                #The line below is the resources if a person does decide to pass
                person.newResourceVector = [person.resourceVector[0]-0.05, person.resourceVector[1]-0.4, line[indx-1].resourceVector[2]]
                print 'Action cost: ' , str(person.actionCost())
                if person.actionCost() > 0:
                    person.nextAction = 'Pass'
                    person.computeEmotion(0.95) #0.95 is the degree of certaininty. TODO: We have to find a way to compute it. 

        displayLine()
        gameStatus = 'protest?'


    elif gameStatus == 'protest?':
        print 'Game status: ' , gameStatus
        for indx, person in reverse_enumerate(line): #going in reverse to avoid the case of someone protesting when the next person has switched actions
            person.halveEmotion()
            if indx < (len(line)-1):
                if line[indx+1].nextAction == "Pass":
                    print "Someoen passing " , person.name
                    person.newResourceVector = [person.resourceVector[0]-0.05, person.resourceVector[1]-0.10, person.resourceVector[2]]
                    print "\n\n\n Action Cost: " + str(person.actionCost())
                    print "\n\n\n Wait Cost: " + str(person.waitCost())
                    if person.actionCost() > person.waitCost():
                        person.nextAction = 'Protest'
                        person.computeEmotion(0.95)
                    else:
                        person.nextAction = "Wait"
                        person.newResourceVector = [person.resourceVector[0], person.resourceVector[1], line[indx+1].resourceVector[2]]
                        person.computeEmotion(0.95)

        displayLine()
        gameStatus = 'penultimate'

    elif gameStatus == 'penultimate':
        print 'The game status is ' , gameStatus
        for indx, person in enumerate(line):
            person.halveEmotion()
            if indx != 0:
                if person.nextAction == 'Pass' and line[indx-1].nextAction == 'Protest':
                    if random() < 0.50:
                        print 'Being protested'
                        person.nextAction = 'Pass_Success'
                        person.computeEmotion(1)
                        line[indx-1].nextAction = 'Wait'
                        line[indx-1].newResourceVector[2] = line[indx].resourceVector[2] #The person goes back
                        line[indx-1].computeEmotion(1)
                        person.resourceVector = person.newResourceVector   #This is to make the new resources as the current resources
                        line[indx-1].resourceVector = line[indx-1].newResourceVector
                        line[indx], line[indx-1] = line[indx-1], line[indx] #Code to swap the 2 positions
                    else:
                        person.nextAction = 'Pass_Fail'
                        person.resourceVector = [person.newResourceVector[0], person.newResourceVector[1], person.resourceVector[2]]
                    person.computeEmotion(1)
                elif person.nextAction == 'Pass' and line[indx-1].nextAction == 'Wait':
                    print 'Not being protested'
                    person.nextAction = 'Pass_Success'
                    person.computeEmotion(1)
                    line[indx-1].computeEmotion(1)
                    line[indx-1].resourceVector = line[indx-1].newResourceVector
                    person.resourceVector = person.newResourceVector   #This is to make the new resources as the current resources
                    line[indx], line[indx-1] = line[indx-1], line[indx] #Code to swap the 2 positions

#                    person.computeEmotion(1)

        for index, person in enumerate(line):
            #This is to add the list of all places where the animation has to happen. To be passed to the html. 
            if(person.getAction() == 'Pass_Success'):
                passing_people.append(index + 1) # +2 because they already made the pass, and the css is indexed from 1
        displayLine()
        gameStatus = 'final'

    elif gameStatus == 'final':
        print '\nThe game status is ' , gameStatus
        print str(line[0].name) , 'gets the Occulus Rift'
        line.pop(0)
        for indx, person in enumerate(line):
            person.halveEmotion()
            person.nextAction = 'Wait'
            person.newResourceVector = [person.resourceVector[0], person.resourceVector[1], 1.0/(indx+1)]
            person.computeEmotion(1)
            person.resourceVector = person.newResourceVector
        displayLine()
        gameStatus = 'initial'

    npc_names = get_npc_names()
    npc_actions = get_npc_actions()
    npc_emotions = get_npc_emotions()
    npc_health = get_npc_health()
    npc_count = len(line)

    print npc_health

    json_response = {
        'names':npc_names,
        'actions':npc_actions,
        'emotions':npc_emotions,
        'health':npc_health,
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

def get_npc_health():
    global line
    new_list = []
    for npc in line:
        new_list.append(npc.resourceVector[0]*100)
    return new_list



