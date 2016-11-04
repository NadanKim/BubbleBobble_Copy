from pico2d import *

import game_framework
import title_state


name = "ScoreState"

font = None
board = None
list = []


def enter():
    global font, board, list
    font = load_font('sprite\\surround\\Pixel.ttf', 30)
    #board = load_image('blackboard.png')
    #file = open('score_data.txt', 'r')
    #list = json.load(file)
    #file.close()


def exit():
    global font, board

    del(font)
    del(board)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.change_state(title_state)


def update():
    pass


def draw_list():
    i = 0
    font.draw(10, 500, '[RANKING]', (255, 0, 0))
    for data in list:
        font.draw(10,  400 - i * 30, '%d : player %d, x:%3d, y:%3d, time:%3.2f'\
                  %(i+1, data['number'], data['x'], data['y'], data['time']), (255, 255, 255))
        i += 1


def draw():
    clear_canvas()
    #board.draw(400, 300)
    #draw_list()
    update_canvas()





