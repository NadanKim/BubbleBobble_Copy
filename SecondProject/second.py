from pico2d import *
import random

# Game object class here
class BOY:
    runimage = None
    def __init__(self):
        self.x, self.y = random.randint(-300, 100), 90
        self.frame = random.randint(0,7)
        self.stayimage = load_image('character.png')
        self.runimage = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame+1) % 8
        self.x += 5

    def draw(self):
        self.runimage.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

class GRASS:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

class BALL:
    image = None
    down = True
    maxHeight = 600
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(600, 700)
        self.dy = random.randint(5, 20)
        self.image = load_image('ball41x41.png')

    def update(self):
        if 80 < self.y and self.down:
            self.y -= self.dy
            if self.y <= 80:
                self.down = False
        elif self.y < self.maxHeight and self.down==False:
            self.y += self.dy
            if self.maxHeight<= self.y:
                self.down = True
                self.maxHeight /= 2

    def draw(self):
        self.image.draw(self.x, self.y)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# initialization code
open_canvas()
team = [BOY() for i in range(11)]
ballRain = [BALL() for i in range(20)]
grass = GRASS()
running = True

# game main loop code
while running:
    handle_events()

    for boy in team:
        boy.update()
    for ball in ballRain:
        ball.update()

    clear_canvas()
    grass.draw()
    for ball in ballRain:
        ball.draw()
    for boy in team:
        boy.draw()
    update_canvas()

    delay(0.05)

# finalization code
close_canvas()