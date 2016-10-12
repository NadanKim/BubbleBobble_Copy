from pico2d import *
from CHARACTER import CHARACTER

class EFFECT:
    radius = 50
    frame, totalFrame = 0, 0
    sprite = None
    state, types = None, None
    ACTION_PER_TIME = None
    PIXEL_PER_METER = (10.0 / 0.1)
    NORMALBUBBLE, MAGIC, BOSSATTACK = 200, 201, 202
    STATE_FLY, STATE_NORMAL, STATE_NORMAL_PINK, STATE_NORMAL_RED, STATE_THUNDER = None, None, None, None, None
    STATE_THUNDER_PINK, STATE_THUNDER_RED, STATE_WATER, STATE_WATER_PINK, STATE_WATER_RED = None, None, None, None, None
    STATE_FIRE, STATE_FIRE_PINK, STATE_FIRE_RED, STATE_PON, STATE_NONE = None, None, None, None, 99
    def __init__(self, type, x, y, direct, dy, attackRange):
        self.types = type
        self.xFirst, self.x, self.y, self.dy = x, x, y, dy
        self.attackRange = attackRange
        if direct == CHARACTER.DIRECT_LEFT:
            self.movePoint = -1
        else:
            self.movePoint = 1
        if type == self.NORMALBUBBLE:
            self.xSprite, self.ySprite = 14, 16
            self.numSprite = 6
            self.MOVE_SPEED_KMPH = 25.0
            self.ACTION_PER_TIME = 1.0 / 1.5
            self.sprite = load_image('sprite\\Effect\\bubbles.png')
            self.STATE_FLY, self.STATE_NORMAL, self.STATE_NORMAL_PINK, self.STATE_NORMAL_RED, self.STATE_THUNDER = 14, 12, 11, 10, 9
            self.STATE_THUNDER_PINK, self.STATE_THUNDER_RED, self.STATE_WATER, self.STATE_WATER_PINK, self.STATE_WATER_RED = 8, 7, 6, 5, 4
            self.STATE_FIRE, self.STATE_FIRE_PINK, self.STATE_FIRE_RED, self.STATE_PON = 3, 2, 1, 0
            self.change_state(self.STATE_FLY)
        elif type == self.MAGIC:
            self.STATE_FLY, self.STATE_PON = 1, 0
            self.numSprite = 4
            self.xSprite, self.ySprite = 16, 16
            self.MOVE_SPEED_KMPH = 15.0
            self.ACTION_PER_TIME = 1.0 / 1.0
            self.sprite = load_image('sprite\\Effect\\magic.png')
            self.change_state(self.STATE_FLY)
        elif type == self.BOSSATTACK:
            self.STATE_FLY = 1
            self.numSprite = 4
            self.xSprite, self.ySprite = 13, 14
            self.MOVE_SPEED_KMPH = 15.0
            self.ACTION_PER_TIME = 1.0 / 1.0
            self.sprite = load_image('sprite\\Effect\\drunkAttack.png')
            self.change_state(self.STATE_FLY)
        self.MOVE_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.MOVE_SPEED_KMPH)

    def contact_checkX(self, frameTime):
        if self.movePoint == -1:
            if self.x - self.radius / 2 - self.MOVE_SPEED_PPS * frameTime < 0:
                return True
        elif self.movePoint == 1:
            if 1200 < self.x + self.radius / 2 + self.MOVE_SPEED_PPS * frameTime:
                return True
        return False

    def contact_checkY(self):
        if self.dy < 0:
            if self.y - self.radius / 2 - self.dy <= 0:
                return True
        elif 0 < self.dy:
            if 800 <= self.y + self.radius / 2 + self.dy:
                return True
        return False

    def change_state(self, state):
        self.state = state
        self.frame = 0
        self.totalFrame = 0

    def draw(self, frameTime):
        self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * self.state,
                              self.xSprite, self.ySprite, self.x, self.y, self.radius, self.radius)
        self.totalFrame += self.numSprite * self.ACTION_PER_TIME * frameTime
        self.frame = int(self.totalFrame) % self.numSprite

    def update(self, frameTime):
        if self.state == self.STATE_FLY:
            self.x += self.movePoint * self.MOVE_SPEED_PPS * frameTime
            self.y += self.dy
            if self.xFirst + self.attackRange <= self.x:
                self.change_state(self.STATE_NORMAL)
        elif self.state == self.STATE_NORMAL:
            if 48 <= self.totalFrame:
                self.change_state(self.STATE_NORMAL_PINK)
        elif self.state == self.STATE_NORMAL_PINK:
            if 24 <= self.totalFrame:
                self.change_state(self.STATE_NORMAL_RED)
        elif self.state == self.STATE_NORMAL_RED:
            if 10 <= self.totalFrame:
                self.change_state(self.STATE_PON)
        elif self.state == self.STATE_PON:
            if 3 <= self.totalFrame:
                self.change_state(self.STATE_NONE)

        if self.contact_checkX(frameTime):
            self.movePoint = 0
            if self.types == self.NORMALBUBBLE:
                self.change_state(self.STATE_NORMAL)
            elif self.types == self.MAGIC:
                self.change_state(self.STATE_PON)
            elif self.types == self.BOSSATTACK:
                self.change_state(self.STATE_NONE)

        if self.contact_checkY():
            self.change_state(self.STATE_NONE)

    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False

    def __del__(self):
        if not self.sprite == None:
            del(self.sprite)