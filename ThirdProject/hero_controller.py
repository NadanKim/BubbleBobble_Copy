# hero_controller.py : control hero move with left and right key

import random
from pico2d import *

running = None
hero = None

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Hero:
    image = None

    FIRST_SPEED, CHANGE_SPEED, MAX_SPEED = 5, 5, 50
    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3
    GO_UP, GO_DOWN, GO_NOT = 4, 5, 6


    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.state = self.RIGHT_STAND
        self.speed = self.FIRST_SPEED
        self.dash = False
        self.dashCount = 0
        self.heightChange = self.GO_NOT
        if Hero.image == None:
            Hero.image = load_image('animation_sheet.png')

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.state not in (self.RIGHT_RUN, ):
                self.state = self.LEFT_RUN
            else:
                self.state = self.RIGHT_STAND
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state not in (self.LEFT_RUN,):
                self.state = self.RIGHT_RUN
            else:
                self.state = self.LEFT_STAND
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            self.dash = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.heightChange = self.GO_UP
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.heightChange = self.GO_DOWN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.state in (self.LEFT_RUN, ):
                self.state = self.LEFT_STAND
            else:
                self.state = self.RIGHT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RIGHT_RUN, ):
                self.state = self.RIGHT_STAND
            else:
                self.state = self.LEFT_RUN
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_SPACE):
            self.dash = False
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
            self.heightChange = self.GO_NOT
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
            self.heightChange = self.GO_NOT


    def update(self):
        self.dashCount -= 1
        self.frame = (self.frame + 1) % 8
        if self.state == self.LEFT_RUN:
            self.x = max(0, self.x - self.speed)
        elif self.state == self.RIGHT_RUN:
            self.x = min(800, self.x + self.speed)
        if self.dash == True and self.dashCount <= 0:
            self.dashCount = 10
            self.speed = min(self.MAX_SPEED,self.speed + self.CHANGE_SPEED)
        elif self.dash == False and self.dashCount <= 0:
            self.dashCount = 10
            self.speed = max(self.FIRST_SPEED, self.speed - self.CHANGE_SPEED)
        if self.heightChange == self.GO_UP:
            self.y = min(560, self.y + self.speed)
        elif self.heightChange == self.GO_DOWN:
            self.y = max(90, self.y - self.speed)


    def draw(self):
        self.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)


def handle_events():
    global running
    global hero
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            hero.handle_event(event)


def main():

    open_canvas()

    global hero
    global running

    hero = Hero()
    grass = Grass()

    running = True
    while running:
        handle_events()

        hero.update()

        clear_canvas()
        grass.draw()
        hero.draw()
        update_canvas()

        delay(0.05)

    close_canvas()


if __name__ == '__main__':
    main()