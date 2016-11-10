import game_framework
import title_state
from pico2d import *


name = "StartState"
image = None
start_sound = None
logo_time = 0.0


def enter():
    global image, start_sound
    image = load_image('sprite\\surround\\kpu_credit.png')
    start_sound = load_music('GameSound\\Background\\GameTurnedOn.ogg')
    start_sound.set_volume(64)
    start_sound.play()


def exit():
    global image, start_sound
    del(image)
    del(start_sound)
    start_sound = None
    image = None


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
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()


def pause(): pass


def resume(): pass




