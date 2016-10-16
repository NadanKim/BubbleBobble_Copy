import game_framework
from pico2d import *
import main_state


name = "TitleState"
title = None
background = None

#font = Font('sprite\\surround\\Pixel.ttf', 20)
logo_time = 0.0
frame = 0


def enter():
    global background, title
    background = load_image("sprite\\surround\\titleBackground.png")
    title = load_image('sprite\\surround\\title.png')


def exit():
    global title, background #, font
    del(title)
    del(background)



def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            game_framework.change_state(main_state)


def draw():
    clear_canvas()
    background.draw(600, 400)
    title.clip_draw(178*frame, 0, 178, 144, 700, 500, 500, 400)
    #font.draw(600, 300, "GAME START", (255, 255, 255)) #<-- error!!!! why!!!!!!
    update_canvas()


def update():
    global frame
    global logo_time
    delay(0.1)
    logo_time += 0.1
    if logo_time <= 3.5 :
        frame = (frame + 1) % 7
    else:
        frame = 0


def pause():
    pass


def resume():
    pass






