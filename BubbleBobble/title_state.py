import game_framework
from pico2d import *
import main_state
import ranking_state


name = "TitleState"
title = None
background = None
font = None
logo_time = 0.0
frame = 0
select = 250


def enter():
    global background, title, font
    background = load_image("sprite\\surround\\titleBackground.png")
    title = load_image('sprite\\surround\\title.png')
    font = Font('sprite\\surround\\Pixel.ttf', 50)


def exit():
    global title, background, font
    del(title)
    del(background)
    del(font)



def handle_events():
    global select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            select+=100
            if 250<select:
                select = 50
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            select -= 100
            if select < 50:
                select = 250
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            if select == 250:
                game_framework.change_state(main_state)
            elif select == 150:
                game_framework.change_state(ranking_state)
            elif select == 50:
                game_framework.quit()


def draw():
    clear_canvas()
    background.draw(600, 400)
    title.clip_draw(178*frame, 0, 178, 144, 700, 500, 500, 400)
    font.draw(600, 250, "GAME START", (255, 255, 255))
    font.draw(600, 150, "RANKING", (255, 255, 255))
    font.draw(600, 50, "EXIT", (255, 255, 255))
    font.draw(540, select, ">>", (255, 255, 255))
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






