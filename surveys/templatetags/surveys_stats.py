from django import template
import pdb

register = template.Library()

@register.filter(name='percentage')
def percentage(answer_objects, index):
    #value is the list of all the objects
    #arg is the index of the 
    local_votes = answer_objects[index - 1].votes
    total_votes = 0

    for obj in answer_objects:
        total_votes += obj.votes

    #pdb.set_trace()
    return (local_votes*100)//total_votes

@register.filter(name="count_votes")
def count_votes(object_list):
    count = 0
    for obj in object_list:
        count += obj.votes

    return count

@register.filter(name="calc_average")
def calc_average(object_list):
    vote_sum = 0.0
    vote_count = 0
    for (counter,obj) in enumerate(object_list):
        vote_sum += (counter + 1) * obj.votes
        vote_count += obj.votes
    return  (float) ((vote_sum*100)//vote_count)/100
