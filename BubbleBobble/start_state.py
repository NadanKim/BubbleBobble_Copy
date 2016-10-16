import game_framework
import title_state
from pico2d import *


name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('sprite\\surround\\kpu_credit.png')


def exit():
    global image
    del(image)


def update():
    global logo_time

    if ( 0.8 < logo_time):
        logo_time = 0
        game_framework.push_state(title_state)
    delay(0.01)
    logo_time += 0.01


def draw():
    clear_canvas()
    image.draw(600, 400)
    update_canvas()




def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




