from pico2d import *

class BOTTLE:
    sprite = None
    TYPE = 'BOTTLE'
    RADIUS = 50
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 40.0
    ACTION_PER_TIME = 1.0 / 1.5
    DIRECT_LEFT, DIRECT_RIGHT = 0, 1
    STATE_FLY, STATE_NONE, STATE_BOOM = 1, 99, None
    def __init__(self, x, y, dy, direct):
        self.frame, self.totalFrame = 0, 0
        self.frameTime = 0
        self.x, self.y = x, y
        self.dy = dy
        self.direct = direct
        self.state = self.STATE_FLY
        self.moveSpeedPPS = 0.0
        self.change_moveSpeed()
        if BOTTLE.sprite == None:
            self.sprite = load_image('sprite\\Effect\\bottle.png')
        self.xSprite, self.ySprite = 13, 14
        self.numSprite = 4


    def change_moveSpeed(self):
        moveSpeedMPM = self.MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        self.moveSpeedPPS = moveSpeedMPS * self.PIXEL_PER_METER


    def get_bb(self):
        return self.x - self.RADIUS / 2, self.y - self.RADIUS / 2, self.x + self.RADIUS / 2, self.y + self.RADIUS / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def draw(self):
        if self.state == self.STATE_FLY:
            self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (self.state - self.direct), self.xSprite, self.ySprite, self.x, self.y, self.RADIUS, self.RADIUS)


    def handle_fly(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = self.x - self.moveSpeedPPS * self.frameTime
        else:
            self.x = self.x + self.moveSpeedPPS * self.frameTime
        self.y += self.dy * self.moveSpeedPPS * self.frameTime
        if self.x <= -self.RADIUS/2 or 1200 + self.RADIUS/2 <= self.x or self.y <= -self.RADIUS/2 or 800 + self.RADIUS/2 <= self.y:
            self.totalFrame = self.frame = 0
            self.state = self.STATE_NONE


    def handle_none(self):
        pass


    handle_state = {
        STATE_FLY: handle_fly,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        # change frames
        self.totalFrame += self.numSprite * self.ACTION_PER_TIME * frameTime
        self.frame = int(self.totalFrame) % self.numSprite
        # change state
        self.handle_state[self.state](self)



    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False