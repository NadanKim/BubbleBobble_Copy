from pico2d import *
from MAGIC import MAGIC
import random

class MAGICIAN():
    TYPE = 'MAGICIAN'
    DIRECT_LEFT, DIRECT_RIGHT, DIRECT_UP, DIRECT_DOWN = 0, 1, 2, 3
    JUMP_HEIGHT = 120
    STATE_WALK, STATE_ANGRY, STATE_AFRAID, STATE_DEAD = 15, 13, 11, 9
    STATE_STUCK_GREEN, STATE_STUCK_YELLOW, STATE_STUCK_RED, STATE_PON, STATE_ATTACK, STATE_NONE = 7, 5, 3, 1, 98, 99
    STATE_JUMP, STATE_DOWN = 70, 71
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 20.0
    FLY_SPEED_KMPH = 15.0
    XSIZE, YSIZE = 50, 70
    sprite = None
    attack = None

    def __init__(self, x ,y):
        self.stayTime = 6.0
        self.x = x
        self.y = y
        self.bfY = self.y
        self.spriteCount = 0
        self.moveSpeedPPS = self.change_moveSpeed(self.MOVE_SPEED_KMPH)
        self.flySpeedPPS = self.change_moveSpeed(self.FLY_SPEED_KMPH)
        self.jumpSpeedPPS = self.moveSpeedPPS
        self.direct = random.randint(0, 1)
        self.directTemp = self.direct
        self.stateTemp = self.state = self.STATE_WALK
        self.frame, self.totalFrame = 0, 0
        self.actionPerTime = 0.0
        self.frameTime = 0.0
        self.yAtJump = 0.0
        self.isAttack = False

        if MAGICIAN.sprite == None:
            MAGICIAN.sprite = load_image('sprite\\Enemy\\magician.png')
        self.xSprite = 16
        self.ySprite = 16
        self.numSprite = 12
        if MAGICIAN.attack == None:
            MAGICIAN.attack = load_image('sprite\\Enemy\\magicianAttack.png')
        self.xAttack = 23
        self.yAttack = 16
        self.numAttack = 5
        self.change_actionPerTime()


    def change_moveSpeed(self, MOVE_SPEED_KMPH):
        moveSpeedMPM = MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def change_actionPerTime(self):
        if self.state == self.STATE_STUCK_GREEN or self.state == self.STATE_STUCK_YELLOW or self.state == self.STATE_STUCK_RED:
            timePerAction = 2.5
            self.spriteCount = self.numSprite
        elif self.state == self.STATE_ATTACK:
            timePerAction = 2.0
            self.spriteCount = self.numAttack
        else:
            timePerAction = 1.5
            self.spriteCount = self.numSprite

        self.actionPerTime = 1.0 / timePerAction


    def get_bb(self):
        return self.x - self.XSIZE * 2 / 5, self.y - self.YSIZE / 2, self.x + self.XSIZE * 2 / 5, self.y + self.YSIZE /2


    def get_bb_left(self):
        return self.x - self.XSIZE * 2 / 5


    def get_bb_right(self):
        return self.x + self.XSIZE * 2 / 5


    def get_bb_top(self):
        return self.y + self.YSIZE /2


    def get_bb_bottom(self):
        return self.y - self.YSIZE / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def stuck_by_bubble(self, attackDirect):
        self.totalFrame = 0
        self.state = self.STATE_STUCK_GREEN
        self.direct = self.DIRECT_UP
        self.directTemp = attackDirect


    def handle_walk(self):
        if self.state == self.STATE_DOWN:
            divide = 2
        else:
            divide = 1
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x -  self.moveSpeedPPS * self.frameTime / divide)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime / divide)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT


    def handle_angry(self):
        if self.state == self.STATE_DOWN:
            divide = 2
        else:
            divide = 1
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x -  self.moveSpeedPPS * self.frameTime * 1.5 / divide)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime * 1.5 / divide)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT


    def handle_afraid(self):
        if self.state == self.STATE_DOWN:
            divide = 2
        else:
            divide = 1
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x -  self.moveSpeedPPS * self.frameTime * 0.5 / divide)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime * 0.5 / divide)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT


    def handle_dead(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        self.y += self.jumpSpeedPPS * self.frameTime * 0.5
        if self.frame == 11:
            self.state = self.STATE_NONE


    def handle_jump(self):
        if self.stateTemp == self.STATE_WALK:
            self.handle_walk()
        elif self.stateTemp == self.STATE_ANGRY:
            self.handle_angry()
        elif self.stateTemp == self.STATE_AFRAID:
            self.handle_afraid()
        self.y += self.jumpSpeedPPS * self.frameTime
        if self.JUMP_HEIGHT <= self.y - self.yAtJump:
            self.state = self.STATE_DOWN
        if 675 < self.y - self.YSIZE / 2:
            self.y = self.YSIZE / 2
            self.state = self.STATE_DOWN

    def handle_down(self):
        if self.stateTemp == self.STATE_WALK:
            self.handle_walk()
        elif self.stateTemp == self.STATE_ANGRY:
            self.handle_angry()
        elif self.stateTemp == self.STATE_AFRAID:
            self.handle_afraid()
        self.bfY = self.y
        self.y -= self.jumpSpeedPPS * self.frameTime
        if self.y < -self.YSIZE:
            self.y = 700


    def handle_stuck(self):
        if self.direct == self.DIRECT_UP:
            self.y += self.flySpeedPPS * self.frameTime
            if 700 < self.y:
                self.y = -self.YSIZE
        elif self.direct == self.DIRECT_DOWN:
            self.y -= self.flySpeedPPS * self.frameTime
            if self.y + self.YSIZE < 0:
                self.y = 750 + self.YSIZE
        elif self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.flySpeedPPS * self.frameTime)
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE / 2 - 50, self.x + self.flySpeedPPS * self.frameTime)

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
                self.stateTemp = self.state
                self.change_actionPerTime()


    def handle_pon(self):
        if self.frame == 4:
            self.state = self.STATE_DEAD


    def handle_attack(self):
        if self.frame == 4:
            self.state = self.stateTemp
            self.change_actionPerTime()
            self.isAttack = True


    def handle_none(self):
        pass


    handle_state = {
        STATE_WALK: handle_walk,
        STATE_ANGRY: handle_angry,
        STATE_AFRAID: handle_afraid,
        STATE_DEAD: handle_dead,
        STATE_JUMP: handle_jump,
        STATE_DOWN: handle_down,
        STATE_STUCK_GREEN: handle_stuck,
        STATE_STUCK_YELLOW: handle_stuck,
        STATE_STUCK_RED: handle_stuck,
        STATE_PON: handle_pon,
        STATE_ATTACK: handle_attack,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        #change frames
        self.totalFrame += self.spriteCount * self.actionPerTime * self.frameTime
        self.frame = int(self.totalFrame) % self.spriteCount
        #change state
        if self.stayTime == 0:
            self.handle_state[self.state](self)
        else:
            self.stayTime -= frameTime
            if self.stayTime < 0:
                self.stayTime = 0
        #change it self AI
        if self.totalFrame % 6 <= 0.5 and not self.state == self.STATE_JUMP and not self.state == self.STATE_DOWN and not self.state == self.STATE_DEAD and not self.state == self.STATE_PON and not self.state == self.STATE_NONE and not self.state == self.STATE_STUCK_GREEN and not self.state == self.STATE_STUCK_YELLOW and not self.state == self.STATE_STUCK_RED and not self.state == self.STATE_ATTACK:
            if random.randint(random.randint(0, 1), random.randint(1, 3)) == 1:
                self.direct = self.DIRECT_LEFT
            else:
                self.direct = self.DIRECT_RIGHT
            if  random.randint(random.randint(0, 2), random.randint(2, 5)) == 3:
                self.yAtJump = self.y
                self.state = self.STATE_JUMP
            elif self.stayTime == 0 and not self.stateTemp == self.STATE_AFRAID and random.randint(0, 5) == 1:
                self.frame = self.totalFrame = 0
                self.state = self.STATE_ATTACK
                self.change_actionPerTime()
        #make attack
        if self.isAttack == True:
            self.isAttack = False
            if self.direct == self.DIRECT_LEFT:
                return MAGIC(self.x-self.XSIZE/2, self.y, self.direct)
            else:
                return MAGIC(self.x+self.XSIZE/2, self.y, self.direct)


    def draw(self):
        if self.state == self.STATE_ATTACK:
            if self.stateTemp == self.STATE_WALK:
                self.attack.clip_draw(self.xAttack * self.frame, self.yAttack * (3 - self.direct), self.xAttack, self.yAttack, self.x, self.y, self.XSIZE * (self.xAttack / self.xSprite), self.YSIZE * (self.yAttack / self.ySprite))
            elif self.stateTemp == self.STATE_ANGRY:
                self.attack.clip_draw(self.xAttack * self.frame, self.yAttack * (1 - self.direct), self.xAttack, self.yAttack, self.x, self.y, self.XSIZE * (self.xAttack / self.xSprite), self.YSIZE * (self.yAttack / self.ySprite))
        elif self.state == self.STATE_JUMP or self.state == self.STATE_DOWN:
            self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (self.stateTemp - self.direct), self.xSprite, self.ySprite, self.x, self.y, self.XSIZE, self.YSIZE)
        else:
            self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (self.state - (self.direct % 2)), self.xSprite, self.ySprite, self.x, self.y, self.XSIZE, self.YSIZE)


    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False