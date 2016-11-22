from pico2d import *
from EFFECT import EFFECT

class BUBBLE:
    sprite = None

    RADIUS = 50
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 80.0
    FLY_SPEED_KMPH = 15.0
    ACTION_PER_TIME = 1.0 / 1.2
    ATTACK_NORMAL, ATTACK_THUNDER, ATTACK_WATER, ATTACK_FIRE = 0, 1, 2, 3
    DIRECT_LEFT, DIRECT_RIGHT, DIRECT_UP, DIRECT_DOWN = 0, 1, 2, 3
    STATE_FLY, STATE_NORMAL, STATE_NORMAL_PINK, STATE_NORMAL_RED, STATE_THUNDER = 14, 12, 11, 10, 9
    STATE_THUNDER_PINK, STATE_THUNDER_RED, STATE_WATER, STATE_WATER_PINK, STATE_WATER_RED = 8, 7, 6, 5, 4
    STATE_FIRE, STATE_FIRE_PINK, STATE_FIRE_RED, STATE_PON, STATE_NONE = 3, 2, 1, 0, 99
    def __init__(self, x, y, direct, attackRange, mode):
        self.frame, self.totalFrame = 0, 0
        self.frameTime = 0
        self.x, self.y = x, y
        self.bfX = x
        self.make_effect = False
        self.first_loc_x = x
        self.direct = direct
        self.mode = mode
        self.directTemp = direct
        self.attackRange = attackRange
        self.state = self.STATE_FLY
        self.makeCount = 8
        self.moveSpeedPPS = self.change_moveSpeed(self.MOVE_SPEED_KMPH)
        self.flySpeedPPS = self.change_moveSpeed(self.FLY_SPEED_KMPH)
        if BUBBLE.sprite == None:
            BUBBLE.sprite = load_image('sprite\\Effect\\bubbles.png')
        self.xSprite, self.ySprite = 14, 16
        self.numSprite = 6
        if direct == self.DIRECT_UP:
            if self.mode == self.ATTACK_NORMAL:
                self.state = self.STATE_NORMAL
            elif self.mode == self.ATTACK_THUNDER:
                self.state = self.STATE_THUNDER
            elif self.mode == self.ATTACK_WATER:
                self.state = self.STATE_WATER
            elif self.mode == self.ATTACK_FRIE:
                self.state = self.STATE_FIRE


    def change_moveSpeed(self, MOVE_SPEED_KMPH):
        moveSpeedMPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def get_bb(self):
        if self.state == self.STATE_FLY:
            if self.direct == self.DIRECT_LEFT:
                return self.x - self.RADIUS / 2, self.y - self.RADIUS / 2, self.bfX + self.RADIUS / 2, self.y + self.RADIUS / 2
            elif self.direct == self.DIRECT_RIGHT:
                return self.bfX - self.RADIUS / 2, self.y - self.RADIUS / 2, self.x + self.RADIUS / 2, self.y + self.RADIUS / 2
            else:
                return self.x - self.RADIUS / 2, self.y - self.RADIUS / 2, self.x + self.RADIUS / 2, self.y + self.RADIUS / 2
        else:
            return self.x - self.RADIUS / 2, self.y - self.RADIUS / 2, self.x + self.RADIUS / 2, self.y + self.RADIUS / 2


    def get_bb_left(self):
        if self.state == self.STATE_FLY:
            if self.direct == self.DIRECT_LEFT:
                return self.x - self.RADIUS / 2
            elif self.direct == self.DIRECT_RIGHT:
                return self.bfX - self.RADIUS / 2
            else:
                return self.x - self.RADIUS / 2
        else:
            return self.x - self.RADIUS / 2


    def get_bb_bottom(self):
        return self.y - self.RADIUS / 2


    def get_bb_right(self):
        if self.state == self.STATE_FLY:
            if self.direct == self.DIRECT_LEFT:
                return self.bfX + self.RADIUS / 2
            elif self.direct == self.DIRECT_RIGHT:
                return self.x + self.RADIUS / 2
            else:
                return self.x + self.RADIUS / 2
        else:
            return self.x + self.RADIUS / 2


    def get_bb_top(self):
        return self.y + self.RADIUS / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def touch_enemy(self, kind):
        if kind not in ("BOSS", "SKULL"):
            self.state = self.STATE_NONE
        else:
            self.frame = 0
            self.mode = self.ATTACK_NORMAL
            self.state = self.STATE_PON


    def draw(self):
        self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * self.state,
                              self.xSprite, self.ySprite, self.x, self.y, self.RADIUS, self.RADIUS)


    def handle_fly(self):
        self.bfX = self.x
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.RADIUS/2, self.x - self.moveSpeedPPS * self.frameTime)
        else:
            self.x = min(1200 - self.RADIUS/2, self.x + self.moveSpeedPPS * self.frameTime)
        if self.first_loc_x + self.attackRange + self.moveSpeedPPS * self.frameTime <= self.x or self.x <= self.first_loc_x - self.attackRange - self.moveSpeedPPS * self.frameTime or \
                        self.x == self.RADIUS/2 or self.x == 1200 - self.RADIUS/2:
            if self.direct == self.DIRECT_LEFT:
                self.x = max(self.RADIUS / 2 + 50, self.x + self.moveSpeedPPS * self.frameTime)
            else:
                self.x = min(1200 - self.RADIUS / 2 - 50, self.x - self.moveSpeedPPS * self.frameTime)
            self.totalFrame = self.frame = 0
            if self.mode == self.ATTACK_NORMAL:
                self.state = self.STATE_NORMAL
            elif self.mode == self.ATTACK_THUNDER:
                self.state = self.STATE_THUNDER
            elif self.mode == self.ATTACK_WATER:
                self.state = self.STATE_WATER
            elif self.mode == self.ATTACK_FRIE:
                self.state = self.STATE_FIRE
            self.direct = self.DIRECT_UP


    def handle_normal(self):
        if self.direct == self.DIRECT_UP:
            self.y += self.flySpeedPPS * self.frameTime
            if 700 < self.y:
                self.y = -self.RADIUS
        elif self.direct == self.DIRECT_DOWN:
            self.y -= self.flySpeedPPS * self.frameTime
            if self.y + self.RADIUS < 0:
                self.y = 750 + self.RADIUS
        elif self.direct == self.DIRECT_LEFT:
            self.x = max(self.RADIUS/2 + 50, self.x - self.flySpeedPPS * self.frameTime)
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.RADIUS / 2 - 50, self.x + self.flySpeedPPS * self.frameTime)

        if self.state == self.STATE_NORMAL and 35 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_NORMAL_PINK
        elif self.state == self.STATE_NORMAL_PINK and 14 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_NORMAL_RED
        elif self.state == self.STATE_NORMAL_RED and 7 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_PON


    def handle_thunder(self):
        if self.direct == self.DIRECT_UP:
            self.y += self.flySpeedPPS * self.frameTime
            if 700 < self.y:
                self.y = -self.RADIUS
        elif self.direct == self.DIRECT_DOWN:
            self.y -= self.flySpeedPPS * self.frameTime
            if self.y + self.RADIUS < 0:
                self.y = 750 + self.RADIUS
        elif self.direct == self.DIRECT_LEFT:
            self.x = max(self.RADIUS/2 + 50, self.x - self.flySpeedPPS * self.frameTime)
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.RADIUS / 2 - 50, self.x + self.flySpeedPPS * self.frameTime)

        if self.state == self.STATE_THUNDER and 35 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_THUNDER_PINK
        elif self.state == self.STATE_THUNDER_PINK and 14 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_THUNDER_RED
        elif self.state == self.STATE_THUNDER_RED and 7 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.mode = self.ATTACK_NORMAL
            self.state = self.STATE_PON


    def handle_water(self):
        if self.direct == self.DIRECT_UP:
            self.y += self.flySpeedPPS * self.frameTime
            if 700 < self.y:
                self.y = -self.RADIUS
        elif self.direct == self.DIRECT_DOWN:
            self.y -= self.flySpeedPPS * self.frameTime
            if self.y + self.RADIUS < 0:
                self.y = 750 + self.RADIUS
        elif self.direct == self.DIRECT_LEFT:
            self.x = max(self.RADIUS/2 + 50, self.x - self.flySpeedPPS * self.frameTime)
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.RADIUS / 2 - 50, self.x + self.flySpeedPPS * self.frameTime)

        if self.state == self.STATE_WATER and 35 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_WATER_PINK
        elif self.state == self.STATE_WATER_PINK and 14 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_WATER_RED
        elif self.state == self.STATE_WATER_RED and 7 <= self.totalFrame:
            self.totalFrame = self.frame = 0
            self.mode = self.ATTACK_NORMAL
            self.state = self.STATE_PON



    def handle_pon(self):
        if self.mode == self.ATTACK_THUNDER:
            self.state = self.STATE_NONE
            self.make_effect = True
        elif self.mode == self.ATTACK_WATER:
            self.state = self.STATE_PON
            self.make_effect = True
            self.makeCount -= 1
            if self.makeCount <= 0:
                self.state = self.STATE_NONE
        if self.mode == self.ATTACK_NORMAL and 4 <= self.totalFrame:
            self.state = self.STATE_NONE


    def handle_none(self):
        pass


    handle_state = {
        STATE_FLY: handle_fly,
        STATE_NORMAL: handle_normal,
        STATE_NORMAL_PINK: handle_normal,
        STATE_NORMAL_RED: handle_normal,
        STATE_THUNDER: handle_thunder,
        STATE_THUNDER_PINK: handle_thunder,
        STATE_THUNDER_RED: handle_thunder,
        STATE_WATER: handle_water,
        STATE_WATER_PINK: handle_water,
        STATE_WATER_RED: handle_water,
        STATE_PON: handle_pon,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        # change frames
        self.totalFrame += self.numSprite * self.ACTION_PER_TIME * frameTime
        self.frame = int(self.totalFrame) % self.numSprite
        # change state
        self.handle_state[self.state](self)
        # make Effects
        if self.make_effect == True:
            if self.mode == self.ATTACK_THUNDER:
                temp = EFFECT(self.x, self.y, EFFECT.STATE_THUNDER, self.direct)
                return temp
            elif self.mode == self.ATTACK_WATER:
                temp = EFFECT(self.x, self.y, EFFECT.STATE_WATER, self.direct)
                return temp



    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False