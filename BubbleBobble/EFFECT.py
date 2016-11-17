from pico2d import *


class EFFECT:
    THUNDER = None
    WATER = None
    FIRE = None
    PIXEL_PER_METER = (10.0 / 0.3)
    DIRECT_LEFT, DIRECT_RIGHT, DIRECT_UP, DIRECT_DOWN = 0, 1, 2, 3
    STATE_THUNDER, STATE_THUNDER_POW, STATE_WATER, STATE_FIRE, STATE_NONE = 0, 1, 2, 3, 99
    sounds = []
    def __init__(self, x, y, state, direct):
        self.x = x
        self.bfX = x
        self.y = y
        self.frameTime = 0.0
        self.frame = 0
        self.totalFrame = 0.0
        self.direct = direct
        self.directTemp = direct
        if state == self.STATE_WATER:
            self.direct = self.DIRECT_DOWN
        self.state = state
        if state == self.STATE_THUNDER or state == self.STATE_THUNDER_POW:
            self.MOVE_SPEED_KMPH = 80.0
            if state == self.STATE_THUNDER:
                self.ACTION_PER_TIME = 1.0 / 1.0
            else:
                self.ACTION_PER_TIME = 1.0 / 0.5
            self.xSprite = 16
            self.ySprite = 16
            self.numSprite = 6
            self.SIZE = 50
        elif state == self.STATE_WATER:
            self.MOVE_SPEED_KMPH = 35.0
            self.ACTION_PER_TIME = 1.0 / 1.0
            self.xSprite = 8
            self.ySprite = 8
            self.numSprite = 6
            self.SIZE = 25
        self.moveSpeedPPS = self.change_moveSpeed(self.MOVE_SPEED_KMPH)

        if EFFECT.THUNDER == None:
            EFFECT.THUNDER = load_image('sprite\\Effect\\thunderEffect.png')
        if EFFECT.WATER == None:
            EFFECT.WATER = load_image('sprite\\Effect\\waterEffect.png')

        self.sounds.append(load_wav('GameSound\\Character\\thunderBubble.wav'))
        self.sounds[0].set_volume(20)


    def change_moveSpeed(self, MOVE_SPEED_KMPH):
        moveSpeedMPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def handle_thunder(self):
        self.bfX = self.x
        if self.direct == self.DIRECT_LEFT:
            self.x = self.x - self.moveSpeedPPS * self.frameTime
            if self.x < -self.SIZE:
                self.state = self.STATE_NONE
        elif self.direct == self.DIRECT_RIGHT:
            self.x = self.x + self.moveSpeedPPS * self.frameTime
            if 1200 + self.SIZE < self.x:
                self.state = self.STATE_NONE


    def handle_thunder_pow(self):
        if 6 <= self.totalFrame:
            self.state = self.STATE_NONE


    def handle_water(self):
        if self.x == self.SIZE / 2 + 50:
            self.direct = self.directTemp = self.DIRECT_RIGHT
        elif self.x == 1200 - self.SIZE / 2 - 50:
                self.direct = self.directTemp = self.DIRECT_LEFT
        if self.direct == self.DIRECT_DOWN:
            self.y -= self.moveSpeedPPS * self.frameTime
        elif self.direct == self.DIRECT_LEFT:
            self.x = max(self.SIZE / 2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.SIZE / 2 - 50, self.x + self.moveSpeedPPS * self.frameTime)

        if self.y < -self.SIZE:
            self.state = self.STATE_NONE


    def handle_none(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.SIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
            if self.x == self.SIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.SIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime)
            if self.x == 1200 - self.SIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        elif self.direct == self.DIRECT_DOWN:
            self.y = self.y - self.moveSpeedPPS * self.frameTime
            if self.y + self.SIZE < 0:
                self.state = self.STATE_NONE


    handle_state = {
        STATE_THUNDER: handle_thunder,
        STATE_THUNDER_POW: handle_thunder_pow,
        STATE_WATER: handle_water,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        # change frames
        self.totalFrame += self.numSprite * self.ACTION_PER_TIME * frameTime
        self.frame = int(self.totalFrame) % self.numSprite
        # change state
        self.handle_state[self.state](self)


    def get_bb(self):
        if self.state == self.STATE_THUNDER:
            if self.direct == self.DIRECT_LEFT:
                return self.x - self.SIZE / 2, self.y - self.SIZE / 2, self.bfX + self.SIZE / 2, self.y + self.SIZE / 2
            elif self.direct == self.DIRECT_RIGHT:
                return self.bfX - self.SIZE / 2, self.y - self.SIZE / 2, self.x + self.SIZE / 2, self.y + self.SIZE / 2
            else:
                return self.x - self.SIZE / 2, self.y - self.SIZE / 2, self.x + self.SIZE / 2, self.y + self.SIZE / 2
        else:
            return self.x - self.SIZE / 2, self.y - self.SIZE / 2, self.x + self.SIZE / 2, self.y + self.SIZE / 2


    def get_bb_left(self):
        if self.state == self.STATE_THUNDER:
            if self.direct == self.DIRECT_LEFT:
                return self.x - self.SIZE / 2
            elif self.direct == self.DIRECT_RIGHT:
                return self.bfX - self.SIZE / 2
            else:
                return self.x - self.SIZE / 2
        else:
            return self.x - self.SIZE / 2


    def get_bb_bottom(self):
        return self.y - self.SIZE / 2


    def get_bb_right(self):
        if self.state == self.STATE_THUNDER:
            if self.direct == self.DIRECT_LEFT:
                return self.bfX + self.SIZE / 2
            elif self.direct == self.DIRECT_RIGHT:
                return self.x + self.SIZE / 2
            else:
                return self.x + self.SIZE / 2
        else:
            return self.x + self.SIZE / 2


    def get_bb_top(self):
        return self.y + self.SIZE / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def draw(self):
        if self.state == self.STATE_THUNDER:
            self.THUNDER.clip_draw(self.xSprite * self.frame, self.ySprite,
                              self.xSprite, self.ySprite, self.x, self.y, self.SIZE, self.SIZE)
        elif self.state == self.STATE_THUNDER_POW:
            self.THUNDER.clip_draw(self.xSprite * self.frame, 0,
                                   self.xSprite, self.ySprite, self.x, self.y, self.SIZE, self.SIZE)
        elif self.state == self.STATE_WATER:
            self.WATER.clip_draw(self.xSprite, self.ySprite * self.directTemp,
                              self.xSprite, self.ySprite, self.x, self.y, self.SIZE, self.SIZE)


    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False