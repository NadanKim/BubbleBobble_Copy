from pico2d import *
import random

class ITEM:
    sprite = None
    font = None
    XSIZE, YSIZE = 60, 60
    POINT = [100, 200, 300, 400, 500, 700, 700, 1000, 1200, 1500, 900, 500, 1000, 700, 200]
    KIND_HEALTH, KIND_RUN, KIND_LONG, KIND_FAST, KIND_THUNDER = 10, 11, 12, 13, 14
    STATE_SET, STATE_FONT, STATE_NONE = 0, 1, 99
    DIRECT_DOWN, DIRECT_STAY = 0, 1
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 15.0
    def __init__(self, x, y):
        x = max(50 + self.XSIZE, x)
        x = min(1150 - self.XSIZE, x)
        y = min(750 - self.YSIZE, y)
        self.x, self.y = x, y
        self.fontTime = 0
        self.state = self.STATE_SET
        self.direct = self.DIRECT_DOWN
        self.spriteSize = 16
        self.moveSpeedPPS = self.change_moveSpeed(self.MOVE_SPEED_KMPH)
        self.itemNumber = random.randint(0, 13)
        self.score = self.POINT[self.itemNumber]
        if ITEM.sprite == None:
            ITEM.sprite = load_image('sprite\\Item\\item_use.png')
        if ITEM.font == None:
            ITEM.font = Font('sprite\\surround\\Pixel.ttf', 20)


    def change_moveSpeed(self, currentSpeedKMPH):
        moveSpeedMPM = currentSpeedKMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def draw(self):
        if self.state == self.STATE_SET:
            self.sprite.clip_draw(self.spriteSize * (self.itemNumber % 5), self.spriteSize * (2 - int(self.itemNumber / 5)),\
                                  self.spriteSize, self.spriteSize, self.x, self.y, self.XSIZE, self.YSIZE)
        elif self.state == self.STATE_FONT:
            self.font.draw(self.x, self.y, str(self.score), (40, 255, 40))


    def get_bb(self):
        return self.x - self.XSIZE * 2 / 5, self.y - self.YSIZE / 2, self.x + self.XSIZE * 2 / 5, self.y + self.YSIZE * 2 / 5


    def get_bb_left(self):
        return self.x - self.XSIZE * 2 / 5


    def get_bb_right(self):
        return self.x + self.XSIZE * 2 / 5


    def get_bb_top(self):
        return self.y + self.YSIZE * 2 / 5


    def get_bb_bottom(self):
        return self.y - self.YSIZE / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def update(self, frameTime):
        if self.direct == self.DIRECT_DOWN:
            self.y -= frameTime * self.moveSpeedPPS
            if self.y < self.YSIZE / 2:
                self.y = 800
        if self.state == self.STATE_FONT:
            self.fontTime += frameTime
            self.y += 2
            if 0.7 < self.fontTime:
                self.state = self.STATE_NONE