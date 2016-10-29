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
        # bubble contact stage
        self.contact_check_stage_bubble()
        #player's attack check
        if not self.bubbles == [] and self.bubbles[-1].state == self.bubbles[-1].STATE_FLY:
            for enemy in self.enemies:
                if not enemy.TYPE == 'BOSS' and not enemy.state == enemy.STATE_DEAD and not enemy.state == enemy.STATE_STUCK_GREEN \
                        and not enemy.state == enemy.STATE_STUCK_YELLOW and not enemy.state == enemy.STATE_STUCK_RED and contact_check_two_object(self.bubbles[-1], enemy):
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
                if not enemy.state == enemy.STATE_STUCK_GREEN and not enemy.state == enemy.STATE_STUCK_YELLOW \
                        and not enemy.state == enemy.STATE_STUCK_RED and not enemy.state == enemy.STATE_PON and not enemy.state == enemy.STATE_DEAD \
                        and not enemy.state == enemy.STATE_NONE:
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
            if self.player.state in(self.player.STATE_DEAD, self.player.STATE_BURN, self.player.STATE_STAGEMOVE) or\
                            bubble.state in (bubble.STATE_FLY, bubble.STATE_PON, bubble.STATE_NONE):
                continue
            if contact_check_two_object(bubble, self.player):
                bubble.totalFrame = 0.0
                bubble.state = bubble.STATE_PON
        #player contack stage
        self.contact_check_stage_player()
        #enemy contack stage
        self.contact_check_stage_walker()
        self.contact_check_stage_flying()



    def stageMove(self):
        direct = {
            "DIRECT_RIGHT": self.player.DIRECT_RIGHT,
            "DIRECT_LEFT": self.player.DIRECT_LEFT
        }

        self.bubbles = []
        #get stage data file
        fileDirection = 'Stage\\stage' + str(3) + '.txt'#str(self.currentStage) + '.txt'
        stageDataFile = open(fileDirection, 'r')
        stageData = json.load(stageDataFile)
        stageDataFile.close()
        #Set Player
        self.player.FIRST_LOC_X = stageData['player']['x']
        self.player.FIRST_LOC_Y = stageData['player']['y']
        self.player.direct = direct[stageData['player']['direct']]
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
        #if self.currentStage == 5:
         #   self.currentStage = 1


    def bubble_pon_together(self):
        pass


    def contact_check_stage_player(self):
        for tile in self.stages:
            if not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN \
                    and not self.player.state == self.player.STATE_STAGEMOVE and tile.y < 700:
                # check left or right tile
                if self.player.jumpPoint == 1:
                    if self.player.get_bb_left() < tile.x and tile.x < self.player.get_bb_right():
                        continue
                if self.player.state == self.player.STATE_MOVE or self.player.stateTemp == self.player.STATE_MOVE:
                    if self.player.direct == self.player.DIRECT_LEFT:
                        if tile.get_bb_bottom() < self.player.y and self.player.y < tile.get_bb_top():
                            if tile.get_bb_left() < self.player.get_bb_left() and self.player.get_bb_left() < tile.get_bb_right():
                                self.player.x = tile.get_bb_right() + self.player.XSIZE / 2
                                break
                    elif self.player.direct == self.player.DIRECT_RIGHT:
                        if tile.get_bb_bottom() < self.player.y and self.player.y < tile.get_bb_top():
                            if tile.get_bb_left() < self.player.get_bb_right() and self.player.get_bb_right() < tile.get_bb_right():
                                self.player.x = tile.get_bb_left() - self.player.XSIZE / 2
                                break
        changed = False
        for tile in self.stages:
            if not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN \
                    and not self.player.state == self.player.STATE_STAGEMOVE and tile.y < 700:
                if not self.player.jumpPoint == 1 and tile.y < self.player.bfY - self.player.YSIZE / 2 and contact_check_two_object(
                        self.player, tile):
                    changed = True
                    self.player.y = self.player.YSIZE / 2 + tile.get_bb_y()
                    if self.player.state == self.player.STATE_DOWN:
                        self.player.state = self.player.stateTemp
                    self.player.jumpPoint = 0
        #when not doing jump change state down
        if not self.player.jumpPoint == 1 and not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN \
                and not self.player.state == self.player.STATE_STAGEMOVE and changed == False:
            if not self.player.state == self.player.STATE_DOWN and not self.player.state == self.player.STATE_ATTACK:
                self.player.state = self.player.STATE_DOWN
            self.player.jumpPoint = -1


    def contact_check_stage_walker(self):
        for enemy in self.enemies:
            if not enemy.TYPE in ("WALKER", "MAGICIAN"):
                continue
            for tile in self.stages:
                if not enemy.state == enemy.STATE_DEAD and tile.y < 700:
                    # check left or right tile
                    if enemy.state == enemy.STATE_JUMP:
                        if enemy.get_bb_left() < tile.x and tile.x < enemy.get_bb_right():
                            continue
                    if enemy.state in (enemy.STATE_WALK, enemy.STATE_ANGRY, enemy.STATE_AFRAID) or enemy.stateTemp == (enemy.STATE_WALK, enemy.STATE_ANGRY, enemy.STATE_AFRAID):
                        if enemy.direct == enemy.DIRECT_LEFT:
                            if tile.get_bb_bottom() < enemy.y and enemy.y < tile.get_bb_top():
                                if tile.get_bb_left() < enemy.get_bb_left() and enemy.get_bb_left() < tile.get_bb_right():
                                    enemy.x = tile.get_bb_right() + enemy.XSIZE / 2
                                    enemy.direct = enemy.DIRECT_RIGHT
                                    break
                        elif enemy.direct == enemy.DIRECT_RIGHT:
                            if tile.get_bb_bottom() < enemy.y and enemy.y < tile.get_bb_top():
                                if tile.get_bb_left() < enemy.get_bb_right() and enemy.get_bb_right() < tile.get_bb_right():
                                    enemy.x = tile.get_bb_left() - enemy.XSIZE / 2
                                    enemy.direct = enemy.DIRECT_LEFT
                                    break
            changed = False
            for tile in self.stages:
                if not enemy.state == enemy.STATE_DEAD and tile.y < 700:
                    if enemy.state == enemy.STATE_DOWN and tile.y < enemy.bfY - enemy.YSIZE / 2 and contact_check_two_object(enemy, tile):
                        changed = True
                        enemy.y = enemy.YSIZE / 2 + tile.get_bb_y()
                        if enemy.state == enemy.STATE_DOWN:
                            enemy.state = enemy.stateTemp
                            enemy.change_actionPerTime()
            #when not doing jump change state down
            if not enemy.state == enemy.STATE_JUMP and not enemy.state == enemy.STATE_DEAD and changed == False:
                if not enemy.state == enemy.STATE_DOWN and not enemy.state == enemy.STATE_PON and not enemy.state == enemy.STATE_NONE \
                        and not enemy.state == enemy.STATE_STUCK_GREEN and not enemy.state == enemy.STATE_STUCK_YELLOW and not enemy.state == enemy.STATE_STUCK_RED \
                        and not enemy.state == enemy.STATE_ATTACK:
                    enemy.stateTemp = enemy.state
                    enemy.state = enemy.STATE_DOWN



    def contact_check_stage_flying(self):
        for enemy in self.enemies:
            if enemy.TYPE in ("WALKER", "MAGICIAN", "BOSS"):
                continue
            for tile in self.stages:
                if not enemy.state == enemy.STATE_DEAD:
                    # check left or right tile
                    if enemy.state in (enemy.STATE_WALK, enemy.STATE_ANGRY, enemy.STATE_AFRAID) or\
                                    enemy.stateTemp in (enemy.STATE_WALK, enemy.STATE_ANGRY, enemy.STATE_AFRAID):
                        if enemy.direct == enemy.DIRECT_LEFT:
                            if tile.get_bb_bottom() < enemy.y and enemy.y < tile.get_bb_top():
                                if tile.get_bb_left() < enemy.x - enemy.XSIZE / 2 and enemy.x - enemy.XSIZE / 2 < tile.get_bb_right():
                                    enemy.x = tile.get_bb_right() + enemy.XSIZE / 2
                                    enemy.direct = enemy.DIRECT_RIGHT
                                    break
                        elif enemy.direct == enemy.DIRECT_RIGHT:
                            if tile.get_bb_bottom() < enemy.y and enemy.y < tile.get_bb_top():
                                if tile.get_bb_left() < enemy.x + enemy.XSIZE / 2 and enemy.x + enemy.XSIZE / 2 < tile.get_bb_right():
                                    enemy.x = tile.get_bb_left() - enemy.XSIZE / 2
                                    enemy.direct = enemy.DIRECT_LEFT
                                    break
            for tile in self.stages:
                if not enemy.state == enemy.STATE_DEAD:
                    # check top or bottom tile
                    if enemy.state in (enemy.STATE_WALK, enemy.STATE_ANGRY, enemy.STATE_AFRAID) or \
                                    enemy.stateTemp in (enemy.STATE_WALK, enemy.STATE_ANGRY, enemy.STATE_AFRAID):
                        if enemy.yDirect == enemy.DIRECT_UP:
                            if tile.get_bb_left() < enemy.x and enemy.x < tile.get_bb_right():
                                if tile.get_bb_bottom() < enemy.y + enemy.YSIZE / 2 and enemy.y + enemy.YSIZE / 2 < tile.get_bb_top():
                                    enemy.y = tile.get_bb_bottom() - enemy.YSIZE / 2
                                    enemy.yDirect = enemy.DIRECT_DOWN
                                    break
                        elif enemy.yDirect == enemy.DIRECT_DOWN:
                            if tile.get_bb_left() < enemy.x and enemy.x < tile.get_bb_right():
                                if tile.get_bb_bottom() < enemy.y - enemy.YSIZE / 2 and enemy.y - enemy.YSIZE / 2 < tile.get_bb_top():
                                    enemy.y = tile.get_bb_top() + enemy.YSIZE / 2
                                    enemy.yDirect = enemy.DIRECT_UP
                                    break


    def contact_check_stage_bubble(self):
        for bubble in self.bubbles:
            if bubble.state in (bubble.STATE_PON, bubble.STATE_NONE):
                continue
            for tile in self.stages:
                if bubble.direct == bubble.DIRECT_UP:
                    if bubble.y + bubble.RADIUS/2 < tile.y and contact_check_two_object(bubble, tile):
                        bubble.y = tile.get_bb_bottom() - bubble.RADIUS / 2
                        if bubble.x < 600:
                            bubble.direct = bubble.DIRECT_RIGHT
                        else:
                            bubble.direct = bubble.DIRECT_LEFT
                        break
                elif bubble.direct == bubble.DIRECT_LEFT:
                    if bubble.state == bubble.STATE_FLY:
                        if contact_check_two_object(bubble, tile):
                            bubble.x = tile.get_bb_right() + bubble.RADIUS / 2
                            bubble.totalFrame = bubble.frame = 0
                            bubble.state = bubble.STATE_NORMAL
                            bubble.direct = bubble.DIRECT_UP
                    else:
                        if bubble.y + bubble.RADIUS/2 < tile.y and not contact_check_two_object(bubble, tile):
                            bubble.direct = bubble.DIRECT_UP
                elif bubble.direct == bubble.DIRECT_RIGHT:
                    if bubble.state == bubble.STATE_FLY:
                        if contact_check_two_object(bubble, tile):
                            bubble.x = tile.get_bb_left() - bubble.RADIUS / 2
                            bubble.totalFrame = bubble.frame = 0
                            bubble.state = bubble.STATE_NORMAL
                            bubble.direct = bubble.DIRECT_UP
                    else:
                        if bubble.y + bubble.RADIUS/2 < tile.y and not contact_check_two_object(bubble, tile):
                            bubble.direct = bubble.DIRECT_UP


def contact_check_two_object(a, b):
    a_left, a_bottom, a_right, a_top = a.get_bb()
    b_left, b_bottom, b_right, b_top = b.get_bb()
    if b_left <= a_right and a_right <= b_right or b_left <= a_left and a_left <= b_right or a_left <= b_right and b_right <= a_right or a_left <= b_left and b_left <= a_right:
        if b_bottom <= a_top and a_top <= b_top or b_bottom <= a_bottom and a_bottom <= b_top or a_bottom <= b_top and b_top <= a_top or a_bottom <= b_bottom and b_bottom <= a_top:
            return True
    return False