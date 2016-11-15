from pico2d import *
from BUBBLE import BUBBLE
import math

class PLAYER():
    DIRECT_LEFT, DIRECT_RIGHT = 0, 1
    ATTACK_RANGE_MIN, ATTACK_RANGE_MAX = 300, 450
    JUMP_MIN = 120
    ATTACK_TERM_MAX, ATTACK_TERM_MIN = 8, 4
    ATTACK_NORMAL, ATTACK_THUNDER, ATTACK_WATER, ATTACK_FIRE = 0, 1, 2, 3
    STATE_STAY, STATE_MOVE, STATE_DEAD, STATE_ATTACK = 11, 9, 7, 5
    STATE_JUMP, STATE_DOWN, STATE_BURN, STATE_STAGEMOVE = 3, 1, 13, 14
    FIRST_LOC_X, FIRST_LOC_Y = 400, 300
    PIXEL_PER_METER = (10.0 / 0.3)
    MIN_MOVE_SPEED_KMPH, MAX_MOVE_SPEED_KMPH = 20.0, 35.0
    JUMP_SPEED_KMPH = 30.0
    XSIZE, YSIZE = 50, 70
    sprite = None
    stageMove = None
    sounds = []
    def __init__(self):
        self.noDie = False
        self.noDieTime = 0.0
        self.x = self.FIRST_LOC_X
        self.y = self.FIRST_LOC_Y
        self.playerHealth = 3
        self.bfY = self.y
        self.currentSpeedKMPH = self.MIN_MOVE_SPEED_KMPH
        self.moveSpeedPPS = self.change_moveSpeed(self.currentSpeedKMPH)
        self.jumpSpeedPPS = self.change_moveSpeed(self.JUMP_SPEED_KMPH)
        self.direct = self.DIRECT_RIGHT
        self.stateTemp = self.state = self.STATE_STAY
        self.frame, self.totalFrame = 0, 0
        self.frameTime = 0.0

        self.yAtJump = 0.0
        self.timePerAction, self.actionPerTime = 0.0, 0.0
        self.stageMoveDx, self.stageMoveDy = 0.0, 0.0
        self.jumpPoint = 0
        self.spriteCount = 0
        self.bubble = False
        self.score = 0
        self.sounds.append(load_wav('GameSound\\Character\\jump.wav'))
        self.sounds.append(load_wav('GameSound\\Character\\attack.wav'))
        self.sounds.append(load_wav('GameSound\\Character\\down.wav'))
        self.sounds[0].set_volume(60)
        self.sounds[1].set_volume(60)
        self.sounds[2].set_volume(40)

        self.attackMode = self.ATTACK_NORMAL
        self.currentAttackTerm = self.ATTACK_TERM_MAX
        self.couldAttack = 0 #0 then attack possible and one attack then add currentAttackTerm
        self.jumpHeight = self.JUMP_MIN
        self.attackRange = self.ATTACK_RANGE_MIN

        if PLAYER.sprite == None:
            PLAYER.sprite = load_image('sprite\\Character\\character.png')
        self.xSprite = 16
        self.ySprite = 16
        self.numSprite = 16

        if self.stageMove == None:
            self.stageMove = load_image('sprite\\Character\\stagemove.png')
        self.xStageMove = 30
        self.yStageMove = 32
        self.numStageMove = 10

        self.change_actionPerTime()


    def change_actionPerTime(self):
        if self.state == self.STATE_ATTACK:
            self.timePerAction = 1.0
        elif self.state == self.STATE_JUMP:
            self.timePerAction = 1.5
        elif self.state == self.STATE_DEAD:
            self.timePerAction = 2.5
        elif self.state == self.STATE_STAGEMOVE:
            self.timePerAction = 5.0
            self.spriteCount = 10
        else:
            self.timePerAction = 1.0

        if not self.state == self.STATE_STAGEMOVE:
            self.spriteCount = 16

        self.actionPerTime = 1.0 / self.timePerAction


    def change_moveSpeed(self, currentSpeedKMPH):
        moveSpeedMPM = currentSpeedKMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        return moveSpeedMPS * self.PIXEL_PER_METER


    def get_bb(self):
        return self.x - self.XSIZE * 2 / 5, self.y - self.YSIZE / 2, self.x + self.XSIZE * 2 / 5, self.y + self.YSIZE * 2 / 5


    def get_bb_left(self):
        return self.x - self.XSIZE * 2 / 5


    def get_bb_right(self):
        return self.x + self.XSIZE * 2 / 5


    def get_bb_top(self):
        return self.y + self.YSIZE * 2 / 5


    def get_bb_bottom(self):
        return self.y - self.YSIZE / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if not self.state == self.STATE_DEAD and not self.state == self.STATE_STAGEMOVE and not self.state == self.STATE_BURN:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                self.direct = self.DIRECT_LEFT
                if self.jumpPoint == 0:
                    self.stateTemp = self.state = self.STATE_MOVE
                else:
                    self.stateTemp = self.STATE_MOVE
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                self.direct = self.DIRECT_RIGHT
                if self.jumpPoint == 0:
                    self.stateTemp = self.state = self.STATE_MOVE
                else:
                    self.stateTemp = self.STATE_MOVE
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_q):  #attack
                if self.couldAttack == 0:
                    self.frame, self.totalFrame = 0, 0
                    self.state = self.STATE_ATTACK
                    self.couldAttack = self.currentAttackTerm
                    self.bubble = True
                    self.sounds[1].play()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_w):  #jump
                if self.jumpPoint == 0:
                    self.state = self.STATE_JUMP
                    self.yAtJump = self.y
                    self.jumpPoint = 1
                    self.sounds[0].play()

            elif (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT) and self.direct == self.DIRECT_LEFT:
                if self.jumpPoint == 0:
                    self.stateTemp = self.state = self.STATE_STAY
                else:
                    self.stateTemp = self.STATE_STAY

            elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT) and self.direct == self.DIRECT_RIGHT:
                if self.jumpPoint == 0:
                    self.stateTemp = self.state = self.STATE_STAY
                else:
                    self.stateTemp = self.STATE_STAY

            self.change_actionPerTime()


    def handle_stay(self):
        pass


    def handle_move(self):
        if self.state == self.STATE_DOWN:
            divide = 2
        else:
            divide = 1
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x -  self.moveSpeedPPS * self.frameTime / divide)
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime / divide)


    def handle_attack(self):
        if self.jumpPoint == 1: #jumping
            self.handle_jump()
        elif self.jumpPoint == -1: #downing
            self.handle_down()
        elif self.stateTemp == self.STATE_MOVE:
            self.handle_move()
        if 4 <= self.frame: #finish attack motion
            if self.jumpPoint == 1: #while jump
                self.state = self.STATE_JUMP
            elif self.jumpPoint == -1:
                self.state = self.STATE_DOWN
            else:
                self.state = self.stateTemp


    def handle_jump(self):
        if self.stateTemp == self.STATE_MOVE:
            self.handle_move()
        self.y += self.jumpSpeedPPS * self.frameTime
        if self.jumpHeight <= self.y - self.yAtJump:
            self.state = self.STATE_DOWN
            self.jumpPoint = -1


    def handle_down(self):
        if self.stateTemp == self.STATE_MOVE:
            self.handle_move()
        self.bfY = self.y
        self.y -= self.jumpSpeedPPS * self.frameTime
        if self.y < -self.YSIZE:
            self.y = 700


    def handle_burn(self):
        if self.frame == 15:
            self.x = self.FIRST_LOC_X
            self.y = self.FIRST_LOC_Y
            self.direct = self.DIRECT_RIGHT
            self.stateTemp = self.state = self.STATE_STAY
            self.currentSpeedKMPH = self.MIN_MOVE_SPEED_KMPH
            self.moveSpeedPPS = self.change_moveSpeed(self.currentSpeedKMPH)
            self.currentAttackTerm = self.ATTACK_TERM_MAX
            self.jumpPoint = 0
            self.couldAttack = 0
            self.jumpHeight = self.JUMP_MIN
            self.attackRange = self.ATTACK_RANGE_MIN
            self.change_actionPerTime()


    def handle_dead(self):
        if self.frame == 15:
            self.x = self.FIRST_LOC_X
            self.y = self.FIRST_LOC_Y
            self.direct = self.DIRECT_RIGHT
            self.stateTemp = self.state = self.STATE_STAY
            self.currentSpeedKMPH = self.MIN_MOVE_SPEED_KMPH
            self.moveSpeedPPS = self.change_moveSpeed(self.currentSpeedKMPH)
            self.currentAttackTerm = self.ATTACK_TERM_MAX
            self.jumpPoint = 0
            self.couldAttack = 0
            self.jumpHeight = self.JUMP_MIN
            self.attackRange = self.ATTACK_RANGE_MIN
            self.change_actionPerTime()
            self.playerHealth -= 1
            self.attackMode = self.ATTACK_NORMAL
            self.noDieTime = 25.0
            self.noDie = True


    def handle_stageMove(self):
        if self.stageMoveDx == 0 and self.stageMoveDy == 0:
            self.stageMoveDx = math.fabs(self.x - self.FIRST_LOC_X) / 50
            self.stageMoveDy = math.fabs(self.y - self.FIRST_LOC_Y) / 50
        if self.x < self.FIRST_LOC_X:
            self.x += self.stageMoveDx
        elif self.FIRST_LOC_X < self.x:
            self.x -= self.stageMoveDx
        if self.y < self.FIRST_LOC_Y:
            self.y += self.stageMoveDy
        elif self.FIRST_LOC_Y < self.y:
            self.y -= self.stageMoveDy
        if not (self.x == self.FIRST_LOC_X) and math.fabs(self.x - self.FIRST_LOC_X) < self.stageMoveDx:
            self.x = self.FIRST_LOC_X
        if not (self.y == self.FIRST_LOC_Y) and math.fabs(self.y - self.FIRST_LOC_Y) < self.stageMoveDy:
            self.y = self.FIRST_LOC_Y
        if (self.x == self.FIRST_LOC_X) and (self.y == self.FIRST_LOC_Y) and self.frame == 9:
            self.stateTemp = self.state = self.STATE_STAY
            self.jumpPoint = 0
            self.couldAttack = 0
            self.stageMoveDx = self.stageMoveDy = 0
            self.change_actionPerTime()


    handle_state = {
        STATE_STAY: handle_stay,
        STATE_MOVE: handle_move,
        STATE_ATTACK: handle_attack,
        STATE_JUMP: handle_jump,
        STATE_DOWN: handle_down,
        STATE_DEAD: handle_dead,
        STATE_BURN: handle_burn,
        STATE_STAGEMOVE: handle_stageMove
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        if not self.noDieTime == 0:
            self.noDieTime -= 0.5
        elif self.noDieTime <= 0 and self.noDie == True:
            self.noDie = False
        #change frames
        self.totalFrame += self.spriteCount * self.actionPerTime * self.frameTime
        self.frame = int(self.totalFrame) % self.spriteCount
        #change state
        self.handle_state[self.state](self)
        #change terms
        if 0 < self.couldAttack:
            self.couldAttack = max(0, self.couldAttack - 1)
        #make bubble
        if self.bubble == True:
            self.bubble = False
            if self.direct == self.DIRECT_LEFT:
               return BUBBLE(self.x-self.XSIZE/2, self.y, self.direct, self.attackRange, self.attackMode)
            else:
                return BUBBLE(self.x+self.XSIZE/2, self.y, self.direct, self.attackRange, self.attackMode)


    def draw(self):
        if self.state == self.STATE_STAGEMOVE:
            self.stageMove.clip_draw(self.xStageMove * self.frame, self.yStageMove * (1 - self.direct),
                                  self.xStageMove, self.yStageMove, self.x, self.y, self.XSIZE*(self.xStageMove/self.xSprite), self.YSIZE*(self.yStageMove/self.ySprite))
        else:
            if self.noDie == True and self.noDieTime % 2 == 0:
                self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (-1),
                                      self.xSprite, self.ySprite, self.x, self.y, self.XSIZE, self.YSIZE)
            else:
                self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (self.state - self.direct),
                                      self.xSprite, self.ySprite, self.x, self.y, self.XSIZE, self.YSIZE)