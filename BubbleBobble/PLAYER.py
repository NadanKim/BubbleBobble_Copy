from pico2d import *
from CHARACTER import CHARACTER
from EFFECT import EFFECT
import math

class PLAYER(CHARACTER):
    movePoint, jumpPoint = 0, 0
    attackPosible, attackRange = 0, 0
    firstX, firstY = 400, 300
    spDx, spDy = None, None
    yAtJump = None
    NORMALBUBBLE = 200
    RANGE_MIN, RANGE_MAX = 300, 450
    ATTACK_MAX, ATTACK_MIN, ATTACK_CHANGE = 0.6, 0.2, 0.05
    STATE_STAY, STATE_MOVE, STATE_DEAD, STATE_ATTACK = 11, 9, 7, 5
    STATE_JUMP, STATE_DOWN, STATE_BURN, STATE_SPECIAL = 3, 1, 13, 14
    spriteRoute = 'sprite\\Character\\character.png'
    specialRoute = 'sprite\\Character\\stagemove.png'

    PIXEL_PER_METER = (10.0 / 0.2)
    MOVE_SPEED_KMPH = 15.0
    JUMP_SPEED_KMPH = 15.0
    MOVE_SPEED_PPS = CHARACTER.make_pps(PIXEL_PER_METER, MOVE_SPEED_KMPH)
    JUMP_SPEED_PPS = CHARACTER.make_pps(PIXEL_PER_METER, JUMP_SPEED_KMPH)

    TIME_PER_MOVE = 1.0
    TIME_PER_JUMP = 1.5
    TIME_PER_ATTACK = 1.0
    TIME_PER_DEAD = 2.5
    TIME_PER_SPECIAL = 5.0

    def __init__(self):
        self.stateTemp = self.STATE_STAY
        self.attackRate = PLAYER.ATTACK_MAX
        self.jumpHeight = CHARACTER.JUMP_MIN
        self.attackRange = PLAYER.RANGE_MAX
        CHARACTER.__init__(self, self.firstX, self.firstY,self.MOVE_SPEED_PPS, self.JUMP_SPEED_PPS, CHARACTER.XSIZE, CHARACTER.YSIZE, PLAYER.STATE_STAY)
        CHARACTER.init_sprite(self, 16, 16, 16, self.spriteRoute)
        CHARACTER.init_special(self, 30, 32, 10, self.specialRoute)
        CHARACTER.change_APT(self, PLAYER.TIME_PER_MOVE)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                if not self.state == PLAYER.STATE_DEAD and not self.state == PLAYER.STATE_SPECIAL:
                    self.move(PLAYER.DIRECT_LEFT)
            elif event.key == SDLK_RIGHT:
                if not self.state == PLAYER.STATE_DEAD and not self.state == PLAYER.STATE_SPECIAL:
                    self.move(PLAYER.DIRECT_RIGHT)
            elif event.key == SDLK_q:  #attack
                if not self.state == PLAYER.STATE_DEAD and not self.state == PLAYER.STATE_SPECIAL:
                    if self.attackPosible == 0:
                        self.action(PLAYER.STATE_ATTACK)
            elif event.key == SDLK_w:  #jump
                if not self.state == PLAYER.STATE_DEAD and not self.state == PLAYER.STATE_SPECIAL:
                    self.action(PLAYER.STATE_JUMP)
                    self.stateTemp = PLAYER.STATE_JUMP
            elif event.key == SDLK_d:
                self.action(PLAYER.STATE_SPECIAL)
        elif event.type == SDL_KEYUP:
            if not self.state == PLAYER.STATE_DEAD and not self.state == PLAYER.STATE_SPECIAL:
                if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                    self.action(PLAYER.STATE_STAY)

    def move(self, direct):
        CHARACTER.change_APT(self, self.TIME_PER_MOVE)
        if direct == self.DIRECT_LEFT:
            self.change_direct(CHARACTER.DIRECT_LEFT)
            self.change_state(PLAYER.STATE_MOVE)
        elif direct == self.DIRECT_RIGHT:
            self.change_direct(CHARACTER.DIRECT_RIGHT)
            self.change_state(PLAYER.STATE_MOVE)

    def action(self, state):
        if state == PLAYER.STATE_STAY:
            self.movePoint = 0
            if self.stateTemp == PLAYER.STATE_JUMP or self.stateTemp == PLAYER.STATE_DOWN:
                self.change_state(self.stateTemp)
            else:
                self.change_state(state)
                self.stateTemp = state
        elif state == PLAYER.STATE_ATTACK:
            self.stateTemp = self.state
            if self.attackPosible == 0:
                self.attackPosible = self.attackRate
                CHARACTER.change_APT(self, PLAYER.TIME_PER_ATTACK)
                self.change_state(self.STATE_ATTACK)
        elif state == PLAYER.STATE_JUMP:
            if self.jumpPoint == 0:
                self.jumpPoint = 1
                self.yAtJump = self.y
                CHARACTER.change_APT(self, PLAYER.TIME_PER_JUMP)
                self.change_state(state)
        elif state == PLAYER.STATE_DOWN:
            self.stateTemp = PLAYER.STATE_DOWN
            self.jumpPoint = -1
            if not self.state == self.STATE_ATTACK:
                self.change_state(state)
        elif state == PLAYER.STATE_DEAD:
            CHARACTER.change_APT(self, PLAYER.TIME_PER_DEAD)
            self.change_state(state)
        elif state == PLAYER.STATE_SPECIAL:
            self.spDx = math.fabs(self.x - self.firstX)/50
            self.spDy = math.fabs(self.y - self.firstY)/50
            self.movePoint = 0
            self.jumpPoint = 0
            CHARACTER.change_APT(self, PLAYER.TIME_PER_SPECIAL)
            self.change_state(state)
        elif state == PLAYER.STATE_BURN:
            self.change_state(state)

    def contact_checkY(self, frameTime):
        if self.jumpPoint == -1:
            if self.y - self.ySize / 2 - self.dx * frameTime <= 0:
                return True
        return False

    def update(self, frameTime):
        if self.state == PLAYER.STATE_DEAD:
            if self.frame == 15:
                self.x = self.firstX
                self.y = self.firstY
                self.movePoint = 0
                self.jumpPoint = 0
                self.change_direct(PLAYER.DIRECT_RIGHT)
                self.action(PLAYER.STATE_STAY)
        else:
            if 0 < self.attackPosible:
                self.attackPosible -= frameTime
                if self.attackPosible < 0:
                    self.attackPosible = 0
            if not self.movePoint == 0 and not self.contact_checkX(frameTime):
                    self.x += self.movePoint * self.dx * frameTime
            if not self.jumpPoint == 0:
                self.y += self.jumpPoint * self.dy * frameTime
                if self.jumpHeight <= self.y-self.yAtJump:
                    self.action(PLAYER.STATE_DOWN)
                    self.stateTemp = PLAYER.STATE_DOWN
                elif self.contact_checkY(frameTime):
                    self.jumpPoint = 0
                    if not self.movePoint == 0:
                        self.change_state(PLAYER.STATE_MOVE)
                        self.stateTemp = PLAYER.STATE_MOVE
                    else:
                        self.change_state(PLAYER.STATE_STAY)
                        self.stateTemp = PLAYER.STATE_STAY
            if self.state == self.STATE_ATTACK:
                if self.frame == 3:
                    self.change_state(self.stateTemp)
                    return EFFECT(PLAYER.NORMALBUBBLE, self.x, self.y, self.direct, 0, self.attackRange)

            if self.state == self.STATE_SPECIAL:
                if self.x < self.firstX:
                    self.x += self.spDx
                elif self.firstX < self.x:
                    self.x -= self.spDx
                if self.y < self.firstY:
                    self.y += self.spDy
                elif self.firstY < self.y:
                    self.y -= self.spDy
                if not (self.x == self.firstX) and math.fabs(self.x - self.firstX) < self.spDx:
                    self.x = self.firstX
                if not (self.y == self.firstY) and math.fabs(self.y - self.firstY) < self.spDy:
                    self.y = self.firstY
                if self.frame == 9:
                    self.change_direct(PLAYER.DIRECT_RIGHT)
                    self.action(PLAYER.STATE_STAY)

    def draw(self, frameTime):
        if self.state == PLAYER.STATE_SPECIAL:
            self.special.clip_draw(self.xSpecial * self.frame, self.ySpecial * (1 - self.direct),
                                  self.xSpecial, self.ySpecial, self.x, self.y, self.xSize*(self.xSpecial/self.xSprite), self.ySize*(self.ySpecial/self.ySprite))
            self.totalFrame += self.numSpecial * self.ACTION_PER_TIME * frameTime
            self.frame = int(self.totalFrame) % self.numSpecial
        else:
            CHARACTER.draw(self, frameTime)
