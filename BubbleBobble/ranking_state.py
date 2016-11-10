from pico2d import *
import json
import copy
import game_framework
import start_state


name = "ScoreState"

font = None
changeBoxX = 792
changeBoxY = 550
board = None
name = []
namePos = 0
list = []
temp = None
ranking_sound = None


def get_bb():
    if name[namePos] == 73:
        return changeBoxX - 20, changeBoxY - 25, changeBoxX - 10, changeBoxY + 25
    else:
        return changeBoxX - 20, changeBoxY - 25, changeBoxX + 20, changeBoxY + 25


def enter():
    global font, board, list, temp, real_list, changeBoxX, name, namePos, ranking_sound
    changeBoxX = 792
    name = [65, 65, 65]
    namePos = 0

    font = load_font('sprite\\surround\\Pixel.ttf', 50)
    board = load_image('sprite\\surround\\background.png')

    file = open('gameData\\ranking_data.txt', 'r')
    list = json.load(file)
    file.close()

    file = open('gameData\\temp_data.txt', 'r')
    temp = json.load(file)
    list.append({'score': temp['score'], 'round': temp['round'], 'name': name})
    file.close()

    ranking_sound = load_music('GameSound\\Background\\Ranking.ogg')
    ranking_sound.set_volume(64)
    ranking_sound.play()

def exit():
    global font, board, list, ranking_sound

    list.sort(key=lambda e: (e['score']), reverse=True)
    list = list[:5]

    file = open('gameData\\ranking_data.txt', 'w')
    json.dump(list, file)
    file.close()

    file = open('gameData\\temp_data.txt', 'w')
    json.dump({"score": 0, "round": 0}, file)
    file.close()

    del(font)
    del(board)
    del(ranking_sound)
    ranking_sound = None


def pause():
    pass


def resume():
    pass


def handle_events():
    global changeBoxX, namePos, list
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(start_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
                game_framework.change_state(start_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if name[namePos] != 73:
                    changeBoxX += 47
                else:
                    changeBoxX += 15.5
                namePos += 1
                if 2 < namePos:
                    changeBoxX = 792
                    namePos = 0
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
                list.pop()
                name[namePos] += 1
                if 90 < name[namePos]:
                    name[namePos] = 65
                list.append({'score': temp['score'], 'round': temp['round'], 'name': name})
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
                list.pop()
                name[namePos] -= 1
                if name[namePos] < 65:
                    name[namePos] = 90
                list.append({'score': temp['score'], 'round': temp['round'], 'name': name})


def update():
    pass


def draw_list():
    real_list = copy.deepcopy(list)
    real_list.sort(key=lambda e: (e['score']), reverse=True)
    real_list = real_list[:5]
    i = 0
    font.draw(200, 680, "ENTER YOUR INITIALS !", (40, 255, 40))
    font.draw(200, 620, "SCORE   ROUND   NAME", (255, 255, 40))
    font.draw(200, 540, "%d" %(temp['score']), (255, 255, 255))
    font.draw(600, 540, "%d" %(temp['round']), (255, 255, 255))
    font.draw(772, 540, "%c%c%c" %(name[0], name[1], name[2]), (255, 255, 255))
    draw_rectangle(*get_bb())
    for data in real_list:
        if i == 0:
            font.draw(120,  400 - i * 60, '%d :'%(i+1), (255, 255, 40))
            font.draw(200, 400 - i * 60, '%d' % (data['score']), (255, 255, 40))
            font.draw(600, 400 - i * 60, '%d' % (data['round']), (255, 255, 40))
            font.draw(772, 400 - i * 60, '%c%c%c' % (data['name'][0], data['name'][1], data['name'][2]), (255, 255, 40))
        else:
            font.draw(120, 400 - i * 60, '%d:' % (i + 1), (255, 255, 255))
            font.draw(200, 400 - i * 60, '%d' % (data['score']), (255, 255, 255))
            font.draw(600, 400 - i * 60, '%d' % (data['round']), (255, 255, 255))
            font.draw(772, 400 - i * 60, '%c%c%c' % (data['name'][0], data['name'][1], data['name'][2]), (255, 255, 255))
        i += 1


def draw():
    clear_canvas()
    board.draw(600, 400)
    draw_list()
    update_canvas()





