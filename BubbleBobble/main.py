from pico2d import *
from PLAYER import PLAYER
from ENEMY import ENEMY

def handle_events():
    global GAMERUN
    global player
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            GAMERUN = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                GAMERUN = False
        else:
            player.handle_event(event)

open_canvas(1200, 800, True)
GAMERUN = True
TIMMING = 0.05
bub = None
effects = []
player = PLAYER()
e1 = ENEMY(ENEMY.WALKER, 100, 100)
e2 = ENEMY(ENEMY.MAGICIAN, 200, 200)
e3 = ENEMY(ENEMY.TADPOLE, 100, 300)
e4 = ENEMY(ENEMY.PURPUR, 200, 400,)
e5 = ENEMY(ENEMY.BOSS, 500, 500)
ees = [e1, e2, e3, e4, e5]
background = load_image("sprite\\srround\\background.png")
currentTime = get_time()
while(GAMERUN):
    frameTime = get_time() - currentTime
    handle_events()
    for enemy in ees:
        bub = enemy.update(frameTime)
        if not bub == None:
            effects.append(bub)
            bub = None
    bub = player.update(frameTime)
    if not bub == None:
        effects.append(bub)
        bub = None
    for effect in effects:
        effect.update(frameTime)
        if effect.isPop():
            del(effect)

    clear_canvas()
    background.draw(600,400,1200, 800)
    player.draw(frameTime)
    for enemy in ees:
        enemy.draw(frameTime)
    for effect in effects:
        effect.draw(frameTime)
    update_canvas()

    currentTime += frameTime
