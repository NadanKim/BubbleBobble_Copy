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
pause = False
over_music = False
select = 0
current_time = get_time()
YES_BUTTON, NO_BUTTON = 420, 840

def enter():
    global stage, background, font, select, pause, over_music
    pause = False
    background = load_image("sprite\\surround\\pauseBackground.png")
    font = load_font('sprite\\surround\\Pixel.ttf', 70)
    over_music = load_music('GameSound\\Background\\GameOver.ogg')
    stage = STAGE()
    select = YES_BUTTON


def exit():
    global background, font, over_music, stage
    file = open('gameData\\temp_data.txt', 'w')
    json.dump({"score": stage.player.score, "round": stage.currentStage}, file)
    file.close()
    for i in range(len(stage.musics)):
        stage.musics.pop()
    del(stage)
    del(background)
    del(font)
    del(over_music)
    font = None
    stage = None
    background = None
    over_music = None



def handle_events():
    global draw_box, special_key, stage, select, pause
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE): # pause
            pause = not pause
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
        elif stage.player.playerHealth < 0 or pause == True:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if select == YES_BUTTON:
                    select = NO_BUTTON
                else:
                    select = YES_BUTTON
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if select == NO_BUTTON:
                    select = YES_BUTTON
                else:
                    select = NO_BUTTON
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                if select == YES_BUTTON:
                    if pause == True:
                        pause = False
                    else:
                        stage.player.playerHealth = 3
                        stage.player.noDieTime = 25.0
                        stage.player.noDie = True
                else:
                    over_music.play()
                    delay(2.5)
                    game_framework.change_state(ranking_state)
        elif not stage.enemies == [] and stage.enemies[0].TYPE == 'BOSS' and stage.enemies[0].state == stage.enemies[0].STATE_DEAD:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                game_framework.change_state(ranking_state)
            else:
                stage.player.handle_event(event)
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
    for bubble in stage.bubbles:
        bubble.draw()
    for attack in stage.attacks:
        attack.draw()
    for item in stage.items:
        item.draw()
    for enemy in stage.enemies:
        enemy.draw()
    for effect in stage.effects:
        effect.draw()
    stage.warp.draw()
    stage.player.draw()

    if draw_box == True:
        draw_bb()

    if not stage.enemies == [] and stage.enemies[0].TYPE == 'BOSS' and \
                    stage.enemies[0].state == stage.enemies[0].STATE_DEAD:
        stage.clearFont.draw(200, 500, "Congratulation!!!", (255, 255, 255))
        stage.clearFont.draw(100, 350, "You Clear This Game!!!", (255, 40, 40))


    if stage.player.playerHealth < 0 or pause == True:
        background.draw(600, 400)
        font.draw(500, 600, "CONTINUE??", (255, 255, 40))
        font.draw(500, 400, "YES    /   NO", (255, 255, 255))
        font.draw(select, 400, ">>", (255, 255, 255))
    update_canvas()



def update():
    delay(0.05)
    frame_time = get_frame_time()
    if 0 <= stage.player.playerHealth and pause == False:
        stage.update(frame_time)
    if not stage.enemies == [] and stage.enemies[0].TYPE == 'BOSS' and \
                    stage.enemies[0].state == stage.enemies[0].STATE_NONE:
        game_framework.change_state(ranking_state)


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
    for effect in stage.effects:
        effect.draw_bb()