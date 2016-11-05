import game_framework
from STAGE import STAGE
from pico2d import *
import ranking_state


name = "MainState"
stage = None
background = None
special_key = False
draw_box = False
font = None
select = 0
current_time = get_time()

def enter():
    global stage, background, font, select
    background = load_image("sprite\\surround\\titleBackground.png")
    font = load_font('sprite\\surround\\Pixel.ttf', 70)
    stage = STAGE()
    select = 420


def exit():
    global background, font
    file = open('gameData\\temp_data.txt', 'w')
    json.dump({"score": stage.player.score, "round": stage.currentStage}, file)
    file.close()
    del(background)
    del(font)
    font = None
    background = None



def handle_events():
    global draw_box, special_key, stage, select
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(ranking_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            pass #PAUSE 구현
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LCTRL):
            special_key = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F10):    #no Die Ctrl F10
            if special_key == True:
                if stage.player.noDie == False:
                    stage.player.noDie = True
                    stage.player.noDieTime = 99999
                else:
                    stage.player.noDie = False
                    stage.player.noDieTime = 0
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F11):    #stage move Ctrl F11
            if special_key == True:
                stage.enemies = []
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_F4):
            if draw_box == True:
                draw_box = False
            else:
                draw_box = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LCTRL):
            special_key = False
        elif stage.player.playerHealth < 0:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if select == 420:
                    select = 840
                else:
                    select = 420
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if select == 840:
                    select = 420
                else:
                    select = 840
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                if select == 420:
                    stage.player.playerHealth = 3
                else:
                    game_framework.change_state(ranking_state)
        else:
            stage.player.handle_event(event)


def get_frame_time():
    global current_time
    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def draw():
    clear_canvas()

    if 0 <= stage.player.playerHealth:
        stage.draw()
        for enemy in stage.enemies:
            enemy.draw()
        for bubble in stage.bubbles:
            bubble.draw()
        for attack in stage.attacks:
            attack.draw()
        for item in stage.items:
            item.draw()
        stage.warp.draw()
        stage.player.draw()

        if draw_box == True:
            draw_bb()
    else:
        background.draw(600, 400)
        font.draw(500, 600, "CONTINUE??", (255, 255, 40))
        font.draw(500, 400, "YES    /   NO", (255, 255, 255))
        font.draw(select, 400, ">>", (255, 255, 255))
    update_canvas()



def update():
    delay(0.05)
    frame_time = get_frame_time()
    if 0 <= stage.player.playerHealth:
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
    for tile in stage.stages:
        tile.draw_bb()
    for item in stage.items:
        item.draw_bb()