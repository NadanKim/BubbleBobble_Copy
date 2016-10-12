from pico2d import *
from CHARACTER import CHARACTER
from EFFECT import EFFECT
import random

class ENEMY(CHARACTER):
    PIXEL_PER_METER = (10.0 / 0.2)
    MOVE_SPEED_KMPH = 12.0
    JUMP_SPEED_KMPH = 12.0

    kind = None
    attackCount = 0
    yAtJump = 0
    WALKER, MAGICIAN, TADPOLE, PURPUR, BOSS = 20, 21, 22, 23, 24
    TIME_PER_NORMAL = 1.5
    TIME_PER_SPECIAL = 2.0
    STATE_WALK, STATE_ANGRY, STATE_AFRAID, STATE_DEAD = None, None, None, None
    STATE_STOCKG, STATE_STOCKY, STATE_STOCKR, STATE_PON = None, None, None, None
    STATE_SPECIAL, STATE_NONE, MAGIC, BOSSATTACK = None, 99, 201, 202
    walkerRoute = "sprite\\Enemy\\walker.png"
    magicianRoute = "sprite\\Enemy\\magician.png"
    magicianSpRoute = "sprite\\Enemy\\magicianAttack.png"
    tadpoleRoute = "sprite\\Enemy\\tadpole.png"
    purpurRoute = "sprite\\Enemy\\purpur.png"
    bossRoute = "D:sprite\\Enemy\\boss.png"

    def __init__(self, number, x, y):
        if number == self.WALKER:
            self.kind = ENEMY.WALKER
            self.MOVE_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.MOVE_SPEED_KMPH)
            self.JUMP_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.JUMP_SPEED_KMPH)
            self.STATE_WALK, self.STATE_ANGRY, self.STATE_AFRAID, self.STATE_DEAD = 15, 13, 11, 9
            self.STATE_STOCKG, self.STATE_STOCKY, self.STATE_STOCKR, self.STATE_PON = 7, 5, 3, 1
            CHARACTER.__init__(self, x, y, self.MOVE_SPEED_PPS, self.JUMP_SPEED_PPS, CHARACTER.XSIZE, CHARACTER.YSIZE, self.STATE_WALK)
            CHARACTER.init_sprite(self, 16, 16, 12, self.walkerRoute)
        elif number == self.MAGICIAN:
            self.kind = ENEMY.MAGICIAN
            self.MOVE_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.MOVE_SPEED_KMPH)
            self.JUMP_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.JUMP_SPEED_KMPH)
            self.STATE_WALK, self.STATE_ANGRY, self.STATE_AFRAID, self.STATE_DEAD = 15, 13, 11, 9
            self.STATE_STOCKG, self.STATE_STOCKY, self.STATE_STOCKR, self.STATE_PON = 7, 5, 3, 1
            self.STATE_SPECIAL =  16
            CHARACTER.__init__(self, x, y, self.MOVE_SPEED_PPS, self.JUMP_SPEED_PPS, CHARACTER.XSIZE, CHARACTER.YSIZE, self.STATE_WALK)
            CHARACTER.init_sprite(self, 16, 16, 12, self.magicianRoute)
            CHARACTER.init_special(self, 23, 16, 5, self.magicianSpRoute)
        elif number == self.TADPOLE:
            self.kind = ENEMY.TADPOLE
            self.MOVE_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.MOVE_SPEED_KMPH)
            self.JUMP_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.JUMP_SPEED_KMPH)
            self.STATE_WALK, self.STATE_ANGRY, self.STATE_AFRAID, self.STATE_SKUL, self.STATE_DEAD = 19, 17, 15, 13, 11
            self.STATE_STOCKG, self.STATE_STOCKY, self.STATE_STOCKR, self.STATE_SMOKE, self.STATE_PON = 9, 7, 5, 3, 1
            CHARACTER.__init__(self, x, y, self.MOVE_SPEED_PPS, self.JUMP_SPEED_PPS, CHARACTER.XSIZE, CHARACTER.YSIZE, self.STATE_WALK)
            CHARACTER.init_sprite(self, 16, 16, 12, self.tadpoleRoute)
        elif number == self.PURPUR:
            self.kind = ENEMY.PURPUR
            self.MOVE_SPEED_KMPH = 25.0
            self.MOVE_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.MOVE_SPEED_KMPH)
            self.JUMP_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.JUMP_SPEED_KMPH)
            self.STATE_WALK, self.STATE_ANGRY, self.STATE_AFRAID, self.STATE_DEAD = 15, 13, 11, 9
            self.STATE_STOCKG, self.STATE_STOCKY, self.STATE_STOCKR, self.STATE_PON = 7, 5, 3, 1
            CHARACTER.__init__(self, x, y, self.MOVE_SPEED_PPS, self.JUMP_SPEED_PPS, CHARACTER.XSIZE, CHARACTER.YSIZE, self.STATE_WALK)
            CHARACTER.init_sprite(self, 16, 16, 12, self.purpurRoute)
        elif number == self.BOSS:
            self.kind = ENEMY.BOSS
            self.MOVE_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.MOVE_SPEED_KMPH)
            self.JUMP_SPEED_PPS = CHARACTER.make_pps(self.PIXEL_PER_METER, self.JUMP_SPEED_KMPH)
            self.STATE_WALK, self.STATE_ANGRY, self.STATE_DEAD, self.STATE_STOCKR, self.STATE_PON = 9, 7, 5, 3, 1
            CHARACTER.__init__(self, x, y, self.MOVE_SPEED_PPS, self.JUMP_SPEED_PPS, CHARACTER.XSIZE*4, CHARACTER.YSIZE*4, self.STATE_WALK)
            CHARACTER.init_sprite(self, 64, 64, 8, self.bossRoute)
        if random.randint(0, 1) == 0:
            self.change_direct(CHARACTER.DIRECT_LEFT)
        else:
            self.change_direct(CHARACTER.DIRECT_RIGHT)
        if not(number == self.WALKER or number == self.MAGICIAN):
            if random.randint(0, 1) == 0:
                self.jumpPoint = -1
            else:
                self.jumpPoint = 1
        else:
            self.jumpPoint = -1
        self.stateTemp = self.STATE_WALK
        self.change_state(self.STATE_WALK)
        CHARACTER.change_APT(self, ENEMY.TIME_PER_NORMAL)

    def contact_checkY(self, frameTime):
        if self.jumpPoint == -1:
            if self.y - self.ySize / 2 - self.dy * frameTime <= 0:
                return True
        elif self.jumpPoint == 1:
            if 800 <= self.y + self.ySize / 2 + self.dy * frameTime:
                return True
        return False

    def update(self, frameTime):

        if self.state == self.STATE_WALK or self.state == self.STATE_ANGRY:
            if self.kind == ENEMY.WALKER or self.kind == ENEMY.MAGICIAN:
                if 15 <= self.totalFrame%16 and self.jumpPoint == 0:
                    if random.randint(0, 1) == 0:
                        self.change_direct(CHARACTER.DIRECT_LEFT)
                    else:
                        self.change_direct(CHARACTER.DIRECT_RIGHT)
                    if random.randint(0, 3) == 1:
                        self.jumpPoint = 1
                        self.yAtJump = self.y

                self.y += self.jumpPoint * self.dy * frameTime
                if CHARACTER.JUMP_MIN <= self.y - self.yAtJump:
                    self.jumpPoint = -1
                elif self.contact_checkY(frameTime):
                    self.jumpPoint = 0

                if self.kind == ENEMY.MAGICIAN and 15 <= self.totalFrame%16 and self.jumpPoint == 0:
                    if random.randint(0, 5) == 1:
                        self.change_state(self.STATE_SPECIAL)

            if self.contact_checkX(frameTime):
                self.attackCount = 0
                if self.direct == CHARACTER.DIRECT_LEFT:
                    self.change_direct(CHARACTER.DIRECT_RIGHT)
                else:
                    self.change_direct(CHARACTER.DIRECT_LEFT)

            if self.contact_checkY(frameTime):
                self.jumpPoint = self.jumpPoint * -1

        if self.state == self.STATE_WALK:
            if not self.movePoint == 0 :
                self.x += self.movePoint * self.dx * frameTime
            if not self.jumpPoint == 0:
                self.y += self.jumpPoint * self.dy * frameTime

        elif self.state == self.STATE_ANGRY:
            if self.direct == CHARACTER.DIRECT_LEFT:
                self.x += -1.2 * self.dx * frameTime
            else:
                self.x += 1.2 * self.dx * frameTime
            if not self.jumpPoint == 0:
                self.y += self.jumpPoint * self.dy * frameTime

        elif self.state == self.STATE_SPECIAL:
            if self.frame == 4:
                self.change_state(self.stateTemp)
                return EFFECT(ENEMY.MAGIC, self.x, self.y, self.direct, 0,1200)

        elif self.state == self.STATE_DEAD:
            if self.direct == CHARACTER.DIRECT_LEFT:
                self.x += -1 * self.dx * frameTime
            else:
                self.x += self.dx * frameTime
            self.y += self.dy * frameTime
            if self.frame == 11:
                self.change_state(ENEMY.STATE_NONE)

        elif self.state == ENEMY.STATE_PON:
            if self.frame == 5:
                self.change_state(ENEMY.STATE_DEAD)

        elif self.state == self.STATE_AFRAID:
            if 72 <= self.totalFrame:
                self.change_state(self.stateTemp)
        elif self.state == self.STATE_STOCKG:
            if 120 <= self.totalFrame :
                self.change_state(ENEMY.STATE_STOCKY)
                self.stateTemp = ENEMY.STATE_ANGRY

        elif self.state == self.STATE_STOCKY:
            if 84 <= self.totalFrame:
                self.change_state(ENEMY.STATE_STOCKR)

        elif self.state == self.STATE_STOCKR:
            if 60 <= self.totalFrame:
                self.change_state(ENEMY.STATE_ANGRY)
                self.stateTemp = ENEMY.STATE_ANGRY

        if self.kind == ENEMY.BOSS and self.frame == 0:
            self.attackCount += 1
            if self.attackCount < 5:
                return EFFECT(ENEMY.BOSSATTACK, self.x+(-1)**(self.direct+1)*self.xSize/2, self.y, self.direct, random.randint(-5,5),1200)

    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False

    def draw(self, frameTime):
        if self.state == self.STATE_SPECIAL:
            if self.stateTemp == self.STATE_WALK:
                self.special.clip_draw(self.xSpecial * self.frame, self.ySpecial * (3 - self.direct),
                                       self.xSpecial, self.ySpecial, self.x, self.y,
                                       self.xSize * (self.xSpecial / self.xSprite),
                                       self.ySize * (self.ySpecial / self.ySprite))
            else:
                self.special.clip_draw(self.xSpecial * self.frame, self.ySpecial * (1 - self.direct),
                                       self.xSpecial, self.ySpecial, self.x, self.y,
                                       self.xSize * (self.xSpecial / self.xSprite),
                                       self.ySize * (self.ySpecial / self.ySprite))
            self.totalFrame += self.numSpecial * self.ACTION_PER_TIME * frameTime
            self.frame = int(self.totalFrame) % self.numSpecial
        elif not self.state == ENEMY.STATE_NONE:
            CHARACTER.draw(self, frameTime)