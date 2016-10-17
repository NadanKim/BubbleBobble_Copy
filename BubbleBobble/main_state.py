import game_framework
from STAGE import STAGE
from pico2d import *


name = "MainState"
stage = None
special_key = False
draw_box = False
current_time = get_time()

def enter():
    global stage
    stage = STAGE()


def exit():
    pass



def handle_events():
    global draw_box, special_key, stage
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_state() #한번 누르면 종료할지 물어보고 엔터 치면 종료 후 start_state 소환
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            pass #PAUSE 구현
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LCTRL):
            special_key = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F10):
            if special_key == True:
                if stage.player.noDie == False:
                    stage.player.noDie = True
                    stage.player.noDieTime = 99999
                else:
                    stage.player.noDie = False
                    stage.player.noDieTime = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F4):
            if draw_box == True:
                draw_box = False
            else:
                draw_box = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LCTRL):
            special_key = False
        else:
            stage.player.handle_event(event)


def get_frame_time():
    global current_time
    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def draw():
    clear_canvas()
    stage.draw()
    for enemy in stage.enemies:
        enemy.draw()
    for bubble in stage.bubbles:
        bubble.draw()
    for attack in stage.attacks:
        attack.draw()
    stage.warp.draw()

    stage.player.draw()

    if draw_box == True:
        draw_bb()
    update_canvas()



def update():
    delay(0.05)
    frame_time = get_frame_time()
    stage.update(frame_time)


def pause():
    pass


def resume():
    pass


def draw_bb():
    stage.player.draw_bb()
    for enemy in stage.enemies:
        enemy.draw_bb()
    for bubble in stage.bubbles:
        bubble.draw_bb()
    for attack in stage.attacks:
        attack.draw_bb()