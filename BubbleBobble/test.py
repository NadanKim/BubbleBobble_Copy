from pico2d import *

open_canvas()

run = True
music = load_music('GameSound\\Background\\MainTheme.ogg')
music.set_volume(64)
music.repeat_play()
effect = load_wav('GameSound\\Character\\attack.wav')

while run:
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            run = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            run = False
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):
            effect.play()

close_canvas()
