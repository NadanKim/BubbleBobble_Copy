from PLAYER import PLAYER
from WALKER import WALKER
from MAGICIAN import MAGICIAN
from TADPOLE import TADPOLE
from PULPUL import PULPUL
from BOSS import BOSS
from WARP import WARP
from TILE import TILE
from pico2d import *
import json

class STAGE:
    background = None
    bigTile = None
    smallTile = None
    def __init__(self):
        self.currentStage = 1
        self.stageMoveCount = 0.0
        self.stageSize = 25
        self.tileSize = 12.5
        self.tileX, tileY = 0, 0
        self.player = PLAYER()
        self.warp = WARP()
        self.bubbles = []
        self.enemies = []
        self.attacks = []
        self.tiles = []
        self.stages = []
        if self.background == None:
            self.background = load_image("sprite\\surround\\background.png")
        if self.bigTile == None:
            self.bigTile = load_image("sprite\\MapTile\\BIGTILE.png")
        if self.smallTile == None:
            self.smallTile = load_image("sprite\\MapTile\\SMALLTILE.png")
        self.stageData = None

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


        if self.enemies == [] and 0 < self.stageMoveCount:
            self.stageMoveCount -= 0.05
        if self.enemies == [] and self.stageMoveCount <= 0:
            self.stageMoveCount = 4.0
            self.warp.warping = True
            self.stageMove()


    def draw(self):
        self.background.draw(600, 400)
        for tile in self.stages:
            tile.draw()


    def contact_check(self):
        #player's attack check
        if not self.bubbles == [] and self.bubbles[-1].state == self.bubbles[-1].STATE_FLY:
            for enemy in self.enemies:
                if not enemy.TYPE == 'BOSS' and not enemy.state == enemy.STATE_DEAD and not enemy.state == enemy.STATE_STUCK_GREEN and not enemy.state == enemy.STATE_STUCK_YELLOW and not enemy.state == enemy.STATE_STUCK_RED and contact_check_two_object(self.bubbles[-1], enemy):
                    enemy.totalFrame = 0
                    enemy.state = enemy.STATE_STUCK_GREEN
                    self.bubbles[-1].state = self.bubbles[-1].STATE_NONE
                    break
                elif enemy.TYPE == 'BOSS' and contact_check_two_object(self.bubbles[-1], enemy):
                    self.bubbles[-1].frame = 0
                    self.bubbles[-1].state = self.bubbles[-1].STATE_PON
                    break
        #enemy's attack check
        if not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN and not self.player.state == self.player.STATE_STAGEMOVE:
            for enemy in self.enemies:
                #enemy is alive
                if not enemy.state == enemy.STATE_STUCK_GREEN and not enemy.state == enemy.STATE_STUCK_YELLOW and not enemy.state == enemy.STATE_STUCK_RED and not enemy.state == enemy.STATE_PON and not enemy.state == enemy.STATE_DEAD and not enemy.state == enemy.STATE_NONE:
                    if self.player.noDie == False and not self.player.state == self.player.STATE_DEAD and contact_check_two_object(self.player, enemy):
                        self.player.frame = self.player.totalFrame = 0
                        self.player.state = self.player.STATE_DEAD
                        self.player.change_actionPerTime()
                #enemy is stucked
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
        #player contack stage
        changed = False
        for tile in self.stages:
            if not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN and not self.player.state == self.player.STATE_STAGEMOVE:
                if not self.player.jumpPoint == 1 and tile.y < 700 and tile.y < self.player.bfY - self.player.YSIZE / 2 and contact_check_two_object(self.player, tile):
                    changed = True
                    self.player.y = self.player.YSIZE / 2 + tile.get_bb_y()
                    if self.player.state == self.player.STATE_DOWN:
                        self.player.state = self.player.stateTemp
                    self.player.jumpPoint = 0
        if not self.player.jumpPoint == 1 and not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN and not self.player.state == self.player.STATE_STAGEMOVE and changed == False:
            if not self.player.state == self.player .STATE_DOWN and not self.player.state == self.player.STATE_ATTACK:
                self.player.state = self.player.STATE_DOWN
            self.player.jumpPoint = -1


    def stageMove(self):
        self.bubbles = []
        #get stage data file
        fileDirection = 'Stage\\stage' + str(self.currentStage) + '.txt'
        stageDataFile = open(fileDirection, 'r')
        stageData = json.load(stageDataFile)
        stageDataFile.close()
        #Set Player
        self.player.FIRST_LOC_X = stageData['player']['x']
        self.player.FIRST_LOC_Y = stageData['player']['y']
        self.player.totalFrame = self.player.frame = 0
        self.player.state = self.player.STATE_STAGEMOVE
        self.player.change_actionPerTime()
        self.currentStage += 1
        self.tileX, self.tileY = 0, 31
        #Summon enemy
        enemyCount = 0
        enemyKind = stageData['enemy']['kind']
        for enemy in enemyKind:
            if enemy == 'WALKER':
                self.enemies.append(WALKER(stageData['enemy']['coordinate'][enemyCount]['x'], stageData['enemy']['coordinate'][enemyCount]['y']))
            elif enemy == 'MAGICIAN':
                self.enemies.append(MAGICIAN(stageData['enemy']['coordinate'][enemyCount]['x'], stageData['enemy']['coordinate'][enemyCount]['y']))
            elif enemy == 'TADPOLE':
                self.enemies.append(TADPOLE(stageData['enemy']['coordinate'][enemyCount]['x'], stageData['enemy']['coordinate'][enemyCount]['y']))
            elif enemy == 'PULPUL':
                self.enemies.append(PULPUL(stageData['enemy']['coordinate'][enemyCount]['x'], stageData['enemy']['coordinate'][enemyCount]['y']))
            elif enemy == 'BOSS':
                self.enemies.append(BOSS(stageData['enemy']['coordinate'][enemyCount]['x'], stageData['enemy']['coordinate'][enemyCount]['y']))
            enemyCount += 1
        #Set Stage
        self.stages = []
        self.tiles = stageData['data']
        for tile in self.tiles:
            if not tile == 0:
                self.stages.append(TILE(tile, self.tileX, self.tileY))
            self.tileX += 1
            if self.tileX == 48:
                self.tileX = 0
                self.tileY -= 1
        if self.currentStage == 4:
            self.currentStage = 1


def contact_check_two_object(a, b):
    a_left, a_bottom, a_right, a_top = a.get_bb()
    b_left, b_bottom, b_right, b_top = b.get_bb()
    if b_left <= a_right and a_right <= b_right or b_left <= a_left and a_left <= b_right or a_left <= b_right and b_right <= a_right or a_left <= b_left and b_left <= a_right:
        if b_bottom <= a_top and a_top <= b_top or b_bottom <= a_bottom and a_bottom <= b_top or a_bottom <= b_top and b_top <= a_top or a_bottom <= b_bottom and b_bottom <= a_top:
            return True
    return False

