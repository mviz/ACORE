from django import template
import pdb
import math

register = template.Library()

@register.filter
def percentage(answer_objects, index):
    #value is the list of all the objects
    #arg is the index of the 
    local_votes = answer_objects[index - 1].votes
    total_votes = 0

    for obj in answer_objects:
        total_votes += obj.votes

    #pdb.set_trace()
    if(total_votes == 0):
        return 0

    return (local_votes*100)//total_votes

@register.filter
def count_votes(object_list):
    count = 0
    for obj in object_list:
        count += obj.votes

    return count

@register.filter
def calc_average(object_list):
    vote_sum = 0.0
    vote_count = 0
    for (counter,obj) in enumerate(object_list):
        vote_sum += (counter + 1) * obj.votes
        vote_count += obj.votes

    if(vote_count == 0):
        return 0

    return  (float) ((vote_sum*100)//vote_count)/100

@register.filter
def mod_calc(n):
    return (n - 1)%3

@register.filter
def format_emotions(weights):
    new_string = ''
    for word in weights:
        for char in word:
            if(char == ':'):
                new_string += ' ['
            else:
                new_string += char
        new_string += '] '

    return new_string


@register.filter
def format_weights(weights):
    new_string = ''
    for val in weights:
        rounded_val = repr(((1000*val)//1)/1000)
        new_string += '[' + rounded_val + '] -- '

    new_string.replace("'",'')
    return new_string[:-3]

@register.filter
def progress_color(index):
    if(index%4==0):
        return ''
    elif(index%4 == 1):
        return 'progress-bar-success'
    elif(index%4 == 2):
        return 'progress-bar-warning'
    elif(index%4 == 3):
        return 'progress-bar-danger'

# FUNCTIONS ARE NO LONGER USED
# @register.filter
# def get_joy_percent(emotions):
#     joy  = emotions[0][4:]
#     joy = float(joy)
#     return int(math.fabs(joy)*100//1)

# @register.filter
# def get_hope_percent(emotions):
#     hope = emotions[1][5:]
#     hope = float(hope)
#     return int(math.fabs(hope)*100//1)

# @register.filter
# def get_sorrow_percent(emotions):
#     sorrow = emotions[2][7:]
#     sorrow = float(sorrow)
#     return int(math.fabs(sorrow)*100//1)

# @register.filter
# def get_fear_percent(emotions):
#     fear = emotions[3][5:]
#     fear = float(fear)
#     return int(math.fabs(fear)*100//1)


# FUNCTION NO LONGER USED
# def getEmotionInt(emotion):
#     for indx, c in enumerate(emotion):
#         if(c == '.'):
#             return int(emotion[(indx+1):])
