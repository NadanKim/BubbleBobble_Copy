from pico2d import *
import math

def handle_events():
    global running
    global direct
    global x
    global y
    global radius
    events = get_events()
    for event in events :
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            x, y=event.x, 600-event.y
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                direct = 1
            elif event.key == SDLK_LEFT:
                direct = 2
            elif event.key == SDLK_UP:
                direct = 3
            elif event.key == SDLK_DOWN:
                direct = 4
            elif event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_a and 20<radius:
                radius=radius-10
            elif event.key == SDLK_d and radius<300:
                radius=radius+10
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT or event.key == SDLK_RIGHT or event.key == SDLK_RIGHT or event.key == SDLK_RIGHT:
                direct = 0



open_canvas()
grass = load_image('grass.png')
character = load_image('run_animation.png')

running = True
radian = 2*3.14/50
currentRadi = 0
x = 400
y = 300
radius=100
frame = 0
direct = 0
while (running):
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 100, 0, 100, 100, x+radius*math.cos(currentRadi), y+radius*math.sin(currentRadi))
    currentRadi=currentRadi+radian
    update_canvas()
    if direct == 1 :
        x = x + 10
        direct = 0
    elif direct == 2 :
        x = x - 10
        direct = 0
    elif direct == 3 :
        y = y + 10
        direct = 0
    elif direct == 4 :
        y = y - 10
        direct = 0
    frame = (frame + 1) % 8

    delay(0.05)
    handle_events()

close_canvas()