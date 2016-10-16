from PLAYER import PLAYER
from WALKER import WALKER
from MAGICIAN import MAGICIAN
from TADPOLE import TADPOLE
from PULPUL import PULPUL
from BOSS import BOSS
from WARP import WARP
from pico2d import *
import json

class STAGE:
    background = None
    def __init__(self):
        self.currentStage = 0
        self.stageMoveCount = 0.0
        self.player = PLAYER()
        self.warp = WARP()
        self.bubbles = []
        self.enemies = []
        self.attacks = []
        if self.background == None:
            self.background = load_image("sprite\\surround\\background.png")
        #self.enemies.append(BOSS())
        self.enemies.append(WALKER())
        self.enemies.append(MAGICIAN())
        self.enemies.append(TADPOLE())
        self.enemies.append(PULPUL())

    def update(self, frame_time):
        bubble = self.player.update(frame_time)
        if not bubble == None:
            self.bubbles.append(bubble)
        for enemy in self.enemies:
            if enemy.isPop():
                self.enemies.remove(enemy)
            else:
                attack = enemy.update(frame_time)
                if not attack == None:
                    self.attacks.append(attack)
        for bubble in self.bubbles:
            if bubble.isPop():
                self.bubbles.remove(bubble)
            else:
                bubble.update(frame_time)
        for attack in self.attacks:
            if attack.isPop():
                self.attacks.remove(attack)
            else:
                attack.update(frame_time)
        self.warp.update()

        self.contact_check()

        if self.enemies == []:
            self.stageMoveCount += 0.05
            if 7.0 <= self.stageMoveCount:
                self.stageMove()


    def contact_check(self):
        #player's attack check
        if not self.bubbles == [] and self.bubbles[-1].state == self.bubbles[-1].STATE_FLY:
            for enemy in self.enemies:
                if not enemy.TYPE == 'BOSS' and not enemy.state == enemy.STATE_STUCK_GREEN and not enemy.state == enemy.STATE_STUCK_YELLOW and not enemy.state == enemy.STATE_STUCK_RED and contact_check_two_object(self.bubbles[-1], enemy):
                    enemy.totalFrame = 0
                    enemy.state = enemy.STATE_STUCK_GREEN
                    self.bubbles[-1].state = self.bubbles[-1].STATE_NONE
                    break
                elif enemy.TYPE == 'BOSS' and contact_check_two_object(self.bubbles[-1], enemy):
                    self.bubbles[-1].frame = 0
                    self.bubbles[-1].state = self.bubbles[-1].STATE_PON
                    break
        #enemy's attack check
        for enemy in self.enemies:
            if not enemy.state == enemy.STATE_STUCK_GREEN and not enemy.state == enemy.STATE_STUCK_YELLOW and not enemy.state == enemy.STATE_STUCK_RED and not enemy.state == enemy.STATE_PON and not enemy.state == enemy.STATE_DEAD and not enemy.state == enemy.STATE_NONE:
                if self.player.noDie == False and not self.player.state == self.player.STATE_DEAD and contact_check_two_object(self.player, enemy):
                    self.player.frame = self.player.totalFrame = 0
                    self.player.state = self.player.STATE_DEAD
                    self.player.change_actionPerTime()
            elif enemy.state == enemy.STATE_STUCK_GREEN or enemy.state == enemy.STATE_STUCK_YELLOW or enemy.state == enemy.STATE_STUCK_RED:
                if contact_check_two_object(self.player, enemy):
                    enemy.frame = enemy.totalFrame = 0
                    enemy.state = enemy.STATE_DEAD
                    enemy.change_actionPerTime()
        for attack in self.attacks:
            if not attack.state == attack.STATE_BOOM and not attack.state == attack.STATE_NONE:
                if self.player.noDie == False and not self.player.state == self.player.STATE_DEAD and contact_check_two_object(self.player, attack):
                    self.player.frame = self.player.totalFrame = 0
                    self.player.state = self.player.STATE_DEAD
                    self.player.change_actionPerTime()
        #bubble contack player
        for bubble in self.bubbles:
            if not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN and not self.player.state == self.player.STATE_STAGEMOVE:
                if not bubble.state == bubble.STATE_FLY and not bubble.state == bubble.STATE_PON and contact_check_two_object(bubble, self.player):
                    bubble.state = bubble.STATE_PON


    def stageMove(self):
        pass


def contact_check_two_object(a, b):
    a_left, a_bottom, a_right, a_top = a.get_bb()
    b_left, b_bottom, b_right, b_top = b.get_bb()
    if b_left <= a_right and a_right <= b_right or b_left <= a_left and a_left <= b_right:
        if b_bottom <= a_top and a_top <= b_top or b_bottom <= a_bottom and a_bottom <= b_top:
            return True
    return False