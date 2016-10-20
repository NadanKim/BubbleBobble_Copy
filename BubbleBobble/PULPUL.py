from pico2d import *
import random

class PULPUL():
    TYPE = 'PULPUL'
    DIRECT_LEFT, DIRECT_RIGHT = 0, 1
    DIRECT_UP, DIRECT_DOWN = 2, 3
    STATE_WALK, STATE_ANGRY, STATE_AFRAID, STATE_DEAD = 15, 13, 11, 9
    STATE_STUCK_GREEN, STATE_STUCK_YELLOW, STATE_STUCK_RED, STATE_PON, STATE_NONE = 7, 5, 3, 1, 99
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 30.0
    MOVEY_SPEED_KMPH = 15.0
    XSIZE, YSIZE = 50, 70
    sprite = None

    def __init__(self, x, y):
        self.stayTime = 6.0
        self.x = x
        self.y = y
        self.moveSpeedPPS = self.change_moveSpeed(self.MOVE_SPEED_KMPH)
        self.moveYSpeedPPS = self.change_moveSpeed(self.MOVEY_SPEED_KMPH)
        self.direct = random.randint(0, 1)
        self.yDirect = random.randint(2, 3)
        self.state = self.STATE_WALK
        self.frame, self.totalFrame = 0, 0
        self.actionPerTime = 0.0
        self.frameTime = 0.0

        if PULPUL.sprite == None:
            PULPUL.sprite = load_image('sprite\\Enemy\\pulpul.png')
        self.xSprite = 16
        self.ySprite = 16
        self.numSprite = 12
        self.change_actionPerTime()


    def change_moveSpeed(self, MOVE_SPEED_KMPH):
        moveSpeedMPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def change_actionPerTime(self):
        if self.state == self.STATE_STUCK_GREEN or self.state == self.STATE_STUCK_YELLOW or self.state == self.STATE_STUCK_RED:
            timePerAction = 2.5
        else:
            timePerAction = 1.5


        self.actionPerTime = 1.0 / timePerAction


    def get_bb(self):
        return self.x - self.XSIZE * 2 / 5, self.y - self.YSIZE / 2, self.x + self.XSIZE * 2 / 5, self.y + self.YSIZE * 2 / 5


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def handle_walk(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        if self.yDirect == self.DIRECT_UP:
            self.y = min(800 - self.YSIZE / 2, self.y + self.moveYSpeedPPS * self.frameTime)
            if self.y == 800 - self.YSIZE / 2:
                self.yDirect = self.DIRECT_DOWN
        elif self.yDirect == self.DIRECT_DOWN:
            self.y = max(self.YSIZE / 2, self.y - self.moveYSpeedPPS * self.frameTime)
            if self.y == self.YSIZE / 2:
                self.yDirect = self.DIRECT_UP



    def handle_angry(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x -  self.moveSpeedPPS * self.frameTime * 1.5)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime * 1.5)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        if self.yDirect == self.DIRECT_UP:
            self.y = min(800 - self.YSIZE / 2, self.y + self.moveYSpeedPPS * self.frameTime * 1.5)
            if self.y == 800 - self.YSIZE / 2:
                self.yDirect = self.DIRECT_DOWN
        elif self.yDirect == self.DIRECT_DOWN:
            self.y = max(self.YSIZE / 2, self.y - self.moveYSpeedPPS * self.frameTime * 1.5)
            if self.y == self.YSIZE / 2:
                self.yDirect = self.DIRECT_UP


    def handle_afraid(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x -  self.moveSpeedPPS * self.frameTime * 0.5)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime * 0.5)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        if self.yDirect == self.DIRECT_UP:
            self.y = min(800 - self.YSIZE / 2, self.y + self.moveYSpeedPPS * self.frameTime * 0.5)
            if self.y == 800 - self.YSIZE / 2:
                self.yDirect = self.DIRECT_DOWN
        elif self.yDirect == self.DIRECT_DOWN:
            self.y = max(self.YSIZE / 2, self.y - self.moveYSpeedPPS * self.frameTime * 0.5)
            if self.y == self.YSIZE / 2:
                self.yDirect = self.DIRECT_UP


    def handle_dead(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        self.y += self.moveSpeedPPS * self.frameTime * 0.5
        if self.frame == 11:
            self.state = self.STATE_NONE


    def handle_stuck(self):
        if self.state == self.STATE_STUCK_GREEN:
            if 80 <= self.totalFrame:
                self.frame = self.totalFrame = 0
                self.state = self.STATE_STUCK_YELLOW
        elif self.state == self.STATE_STUCK_YELLOW:
            if 40 <= self.totalFrame:
                self.frame = self.totalFrame = 0
                self.state = self.STATE_STUCK_RED
        elif self.state == self.STATE_STUCK_RED:
            if 20 <= self.totalFrame:
                check = random.randint( 1, 3)
                self.frame = self.totalFrame = 0
                if check == 1 or check == 2:
                    self.state = self.STATE_ANGRY
                else:
                    self.state = self.STATE_AFRAID
                self.change_actionPerTime()


    def handle_pon(self):
        if self.frame == 4:
            self.state = self.STATE_DEAD


    def handle_none(self):
        pass


    handle_state = {
        STATE_WALK: handle_walk,
        STATE_ANGRY: handle_angry,
        STATE_AFRAID: handle_afraid,
        STATE_DEAD: handle_dead,
        STATE_STUCK_GREEN: handle_stuck,
        STATE_STUCK_YELLOW: handle_stuck,
        STATE_STUCK_RED: handle_stuck,
        STATE_PON: handle_pon,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        #change frames
        self.totalFrame += self.numSprite * self.actionPerTime * self.frameTime
        self.frame = int(self.totalFrame) % self.numSprite
        #change state
        if self.stayTime == 0:
            self.handle_state[self.state](self)
        else:
            self.stayTime -= frameTime
            if self.stayTime < 0:
                self.stayTime = 0


    def draw(self):
        self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (self.state - self.direct), self.xSprite, self.ySprite, self.x, self.y, self.XSIZE, self.YSIZE)


    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False