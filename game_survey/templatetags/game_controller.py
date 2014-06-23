from django import template
import pdb

register = template.Library()

@register.filter(name='user_input')
def update_game(button_pressed, action):
    # use the button_pressed in a switch to decide changes
    # use action to change an element on the page to display the last action taken
    udpate_ncps()
    udpate_story()


def update_npc_

def get_story_text(dummy):
    #funtion that returns the story's next text
    return 'story text' + dummy 

    12345678990klkjsg;lirsbnrtsoihjarf  