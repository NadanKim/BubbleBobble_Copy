from pico2d import *


class EFFECT:
    THUNDER = None
    WATER = None
    FIRE = None
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 80.0
    DIRECT_LEFT, DIRECT_RIGHT = 0, 1
    STATE_THUNDER, STATE_THUNDER_POW, STATE_WATER, STATE_FIRE, STATE_NONE = 0, 1, 2, 3, 99
    def __init__(self, x, y, state, direct):
        self.x = x
        self.y = y
        self.frameTime = 0.0
        self.frame = 0
        self.totalFrame = 0.0
        self.direct = direct
        self.state = state
        self.moveSpeedPPS = self.change_moveSpeed(self.MOVE_SPEED_KMPH)
        if state == self.STATE_THUNDER or state == self.STATE_THUNDER_POW:
            if state == self.STATE_THUNDER:
                self.ACTION_PER_TIME = 1.0 / 1.0
            else:
                self.ACTION_PER_TIME = 1.0 / 0.5
            self.xSprite = 16
            self.ySprite = 16
            self.numSprite = 6
            self.SIZE = 50
        if EFFECT.THUNDER == None:
            EFFECT.THUNDER = load_image('sprite\\Effect\\thunderEffect.png')


    def change_moveSpeed(self, MOVE_SPEED_KMPH):
        moveSpeedMPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def handle_thunder(self):
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


    def handle_none(self):
        pass


    handle_state = {
        STATE_THUNDER: handle_thunder,
        STATE_THUNDER_POW: handle_thunder_pow,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        # change frames
        self.totalFrame += self.numSprite * self.ACTION_PER_TIME * frameTime
        self.frame = int(self.totalFrame) % self.numSprite
        # change state
        self.handle_state[self.state](self)


    def draw(self):
        if self.state == self.STATE_THUNDER:
            self.THUNDER.clip_draw(self.xSprite * self.frame, self.ySprite,
                              self.xSprite, self.ySprite, self.x, self.y, self.SIZE, self.SIZE)
        elif self.state == self.STATE_THUNDER_POW:
            self.THUNDER.clip_draw(self.xSprite * self.frame, 0,
                                   self.xSprite, self.ySprite, self.x, self.y, self.SIZE, self.SIZE)


    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False