from pico2d import *

class CHARACTER:
    DIRECT_LEFT, DIRECT_RIGHT = 0, 1
    XSIZE, YSIZE = 50, 70
    JUMP_MAX, JUMP_MIN, JUMP_CHANGE = 180, 120, 10
    frame = 0
    state = None
    direct = DIRECT_RIGHT
    sprite = None
    special = None
    ACTION_PER_TIME = None
    totalFrame = 0
    jumpPoint = None
    movePoint = None

    def __init__(self, x, y, dx, dy, xsize, ysize, state):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.xSize = xsize
        self.ySize = ysize
        self.state = state

    def init_sprite(self, xImage, yImage, numFrame, route):
        if self.sprite == None:
            self.sprite = load_image(route)
            self.xSprite = xImage
            self.ySprite = yImage
            self.numSprite = numFrame

    def init_special(self, xImage, yImage, numFrame, route):
        if self.special == None:
            self.special = load_image(route)
            self.xSpecial = xImage
            self.ySpecial = yImage
            self.numSpecial = numFrame

    def change_direct(self, direct):
        if direct == self.DIRECT_LEFT:
            self.movePoint = -1
        else:
            self.movePoint = 1
        self.direct = direct

    def change_state(self, state):
        self.state = state
        self.totalFrame = 0

    def change_dy(self, PPS):
        self.dy = PPS

    def make_pps(PIXEL_PER_METER, MOVE_SPEED_KMPH):
        MOVE_SPEED_MPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
        MOVE_SPEED_MPS = MOVE_SPEED_MPM / 60.0
        MOVE_SPEED_PPS = MOVE_SPEED_MPS * PIXEL_PER_METER
        return MOVE_SPEED_PPS

    def change_APT(self, TPA):
        self.ACTION_PER_TIME = 1.0 / TPA

    def draw(self, frameTime):
        self.sprite.clip_draw(self.xSprite*self.frame, self.ySprite*(self.state-self.direct),
                              self.xSprite, self.ySprite, self.x, self.y, self.xSize, self.ySize)
        self.totalFrame += self.numSprite * self.ACTION_PER_TIME * frameTime
        self.frame = int(self.totalFrame) % self.numSprite

    def contact_checkX(self, frameTime):
        if self.direct == CHARACTER.DIRECT_LEFT:
            if self.x - self.xSize/2 - self.dx * frameTime < 0:
                return True
        elif self.direct == CHARACTER.DIRECT_RIGHT:
            if 1200 < self.x + self.xSize/2 + self.dx * frameTime:
                return True
        return False

    def __del__(self):
        if not self.sprite == None:
            del(self.sprite)
        if not self.special == None:
            del(self.special)