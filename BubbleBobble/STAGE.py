from PLAYER import PLAYER
from WALKER import WALKER
from MAGICIAN import MAGICIAN
from TADPOLE import TADPOLE
from PULPUL import PULPUL
from BOSS import BOSS
from WARP import WARP
from TILE import TILE
from EFFECT import EFFECT
from ITEM import ITEM
from SKULL import SKULL
from OBJECT import OBJECT
from pico2d import *
import json
import random



class STAGE:
    background = None
    bigTile = None
    smallTile = None
    font = None
    clearFont = None
    itemSprite = None
    playerHealth = None
    musics = []
    sounds = None
    def __init__(self):
        self.currentStage = 12
        self.stageMoveCount = 0.0
        self.stageSize = 25
        self.tileSize = 12.5
        self.tileX, tileY = 0, 0
        self.player = PLAYER()
        self.player.playerHealth = 3
        self.warp = WARP()
        self.bubbles = []
        self.enemies = []
        self.attacks = []
        self.tiles = []
        self.stages = []
        self.items = []
        self.checkItems = []
        self.effects = []
        self.objects = []
        self.playTime = 0.0
        self.hurry = False
        self.skullAppear = 1
        for i in range(4):
            self.checkItems.append(ITEM(100, 100))
        for i in range(4):
            self.checkItems[i].itemNumber = 11 + i
            self.checkItems[i].x = 1150 - i * 70
            self.checkItems[i].y = 750
        if STAGE.background == None:
            STAGE.background = load_image("sprite\\surround\\background.png")
        if STAGE.bigTile == None:
            STAGE.bigTile = load_image("sprite\\MapTile\\BIGTILE.png")
        if STAGE.smallTile == None:
            STAGE.smallTile = load_image("sprite\\MapTile\\SMALLTILE.png")
        if STAGE.font == None:
            STAGE.font = Font('sprite\\surround\\Pixel.ttf', 30)
        if STAGE.itemSprite == None:
            STAGE.itemSprite = load_image('sprite\\Item\\item_use.png')
        if STAGE.playerHealth == None:
            STAGE.playerHealth = load_image('sprite\\Item\\health.png')
        if STAGE.clearFont == None:
            STAGE.clearFont = Font('sprite\\surround\\Pixel.ttf', 70)
        if STAGE.sounds ==None:
            STAGE.sounds = load_wav('GameSound\\Character\\enemyDown.wav')
            STAGE.sounds.set_volume(40)
        self.musics.append(load_music('GameSound\\Background\\MainTheme.ogg'))
        self.musics.append(load_music('GameSound\\Background\\HurryMainFast.ogg'))
        self.musics.append(load_music('GameSound\\Background\\BossStage.ogg'))
        self.musics.append(load_music('GameSound\\Background\\GameEnding.ogg'))
        self.stageData = None
        self.musics[0].repeat_play()
        file = open('gameData\\ranking_data.txt', 'r')
        data = json.load(file)
        self.highScore = data[0]['score']
        file.close()

    def update(self, frame_time):
        self.playTime += frame_time
        if not self.enemies == [] and self.currentStage != 100 and 30 <= self.playTime and self.hurry == False:
            self.hurry = True
            self.musics[1].play()
        if not self.enemies == [] and self.currentStage != 100 and 45<= self.playTime and 0 < self.skullAppear:
            self.enemies.append(SKULL(random.randint(300, 900), random.randint(300, 500)))
            self.skullAppear -= 1
        bubble = self.player.update(frame_time)
        if not bubble == None:
            self.bubbles.append(bubble)
        for enemy in self.enemies:
            if self.enemies[0].TYPE == 'SKULL' and enemy.state == enemy.STATE_WALK:
                enemy.totalFrame = enemy.frame = 0
                enemy.state = enemy.STATE_DEAD
            if enemy.TYPE == 'SKULL':
                enemy.set_player_loc(self.player.x, self.player.y)
            if enemy.isPop():
                self.items.append(ITEM(enemy.x, enemy.y))
                self.enemies.remove(enemy)
            else:
                attack = enemy.update(frame_time)
                if not attack == None:
                    self.attacks.append(attack)
        for bubble in self.bubbles:
            if bubble.isPop():
                self.bubbles.remove(bubble)
            else:
                effect = bubble.update(frame_time)
                if not effect == None:
                    self.effects.append(effect)
        for attack in self.attacks:
            if attack.isPop():
                self.attacks.remove(attack)
            else:
                attack.update(frame_time)
        for item in self.items:
            item.update(frame_time)
            if item.state == item.STATE_NONE and item.itemNumber != item.KIND_THUNDER:
                self.items.remove(item)
        for effect in self.effects:
            if effect.isPop():
                self.effects.remove(effect)
            else:
                effect.update(frame_time)
        for obj in self.objects:
            bubble = obj.update(frame_time)
            if not bubble == None:
                self.bubbles.append(bubble)


        self.warp.update()
        self.contact_check()


        if self.enemies == [] and 0 < self.stageMoveCount:
            self.stageMoveCount -= 0.05
        if self.enemies == [] and self.stageMoveCount <= 0:
            self.stageMoveCount = 3.0
            self.warp.warping = True
            self.stageMove()


    def draw(self):
        self.background.draw(600, 400)
        for tile in self.stages:
            tile.draw()
        self.background.draw(600, 750, 1200, 100)
        self.font.draw(480, 770, "HIGH SCORE", (255, 30, 30))
        if self.player.score < self.highScore:
            self.font.draw(530, 730, str(self.highScore), (255, 255, 255))
        else:
            self.font.draw(530, 730, str(self.player.score), (255, 255, 255))
        self.font.draw(80, 770, "PLAYER", (40, 255, 40))
        self.font.draw(210 - (len(str(self.player.score))-1)*25, 730, str(self.player.score), (255, 255, 255))
        self.font.draw(1130, 20, str(self.currentStage), (255, 255, 255))
        if self.hurry:
            self.font.draw(440, 360, "HURRY UP!!", (255, 255, 255))

        if self.player.currentSpeedKMPH == self.player.MAX_MOVE_SPEED_KMPH:
            self.checkItems[0].draw()
        if self.player.attackRange == self.player.ATTACK_RANGE_MAX:
            self.checkItems[1].draw()
        if self.player.currentAttackTerm == self.player.ATTACK_TERM_MIN:
            self.checkItems[2].draw()
        if self.player.attackMode == self.player.ATTACK_THUNDER:
            self.checkItems[3].draw()

        for i in range(self.player.playerHealth):
            self.playerHealth.draw(20+i*25, 10, 20, 20)



    def contact_check(self):
        # bubble contact stage
        self.contact_check_stage_bubble()
        self.contact_check_stage_enemyBubble()
        #player's attack check
        self.contact_check_playerattack_enemy()
        #enemy's attack check
        self.contact_check_player_enemy()
        self.contact_check_enemyattack_player()
        #bubble contack player
        self.contact_check_bubble_player()
        #player contack stage
        self.contact_check_stage_player()
        #enemy contack stage
        self.contact_check_stage_walker()
        self.contact_check_stage_flying()
        #enemy attack contact stage
        self.contack_check_stage_enemyAttack()
        #player and item contact check
        self.contact_check_player_item()
        #item and stage contact
        self.contact_check_stage_item()
        #effect and enemy contact
        self.contact_check_effect_enemy()
        #stage and effect contact
        self.contact_check_stage_effect()


    def stageMove(self):
        direct = {
            "DIRECT_RIGHT": self.player.DIRECT_RIGHT,
            "DIRECT_LEFT": self.player.DIRECT_LEFT
        }
        itemKind = {
            "HEALTH": ITEM.KIND_HEALTH,
            "RUN": ITEM.KIND_RUN,
            "LONG": ITEM.KIND_LONG,
            "FAST": ITEM.KIND_FAST,
            "THUNDER": ITEM.KIND_THUNDER
        }
        objKind = {
            "NORMAL": OBJECT.NORMAL,
            "THUNDER": OBJECT.THUNDER,
            "WATER": OBJECT.WATER,
            "FIRE": OBJECT.FIRE,
        }

        self.playTime = 0.0
        self.bubbles = []
        self.items = []
        self.effects = []
        self.currentStage += 1
        self.skullAppear = 1
        if self.hurry:
            self.hurry = False
            self.musics[0].repeat_play()
        if self.currentStage == 14:
            self.currentStage = 100
            self.musics[2].play()
        elif self.currentStage == 101:
            self.currentStage = 0
        #get stage data file
        fileDirection = 'Stage\\stage' + str(self.currentStage) + '.txt'
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
        self.tileX, self.tileY = 0, 31
        #Summon enemy
        Count = 0
        enemyKind = stageData['enemy']['kind']
        for enemy in enemyKind:
            if enemy == 'WALKER':
                self.enemies.append(WALKER(stageData['enemy']['coordinate'][Count]['x'], stageData['enemy']['coordinate'][Count]['y']))
            elif enemy == 'MAGICIAN':
                self.enemies.append(MAGICIAN(stageData['enemy']['coordinate'][Count]['x'], stageData['enemy']['coordinate'][Count]['y']))
            elif enemy == 'TADPOLE':
                self.enemies.append(TADPOLE(stageData['enemy']['coordinate'][Count]['x'], stageData['enemy']['coordinate'][Count]['y']))
            elif enemy == 'PULPUL':
                self.enemies.append(PULPUL(stageData['enemy']['coordinate'][Count]['x'], stageData['enemy']['coordinate'][Count]['y']))
            elif enemy == 'BOSS':
                self.enemies.append(BOSS(stageData['enemy']['coordinate'][Count]['x'], stageData['enemy']['coordinate'][Count]['y']))
            Count += 1
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
        #Set Items
        self.items = []
        itemKinds = stageData['item']['kind']
        Count = 0
        for kind in itemKinds:
            self.items.append(ITEM(stageData['item']['coordinate'][Count]['x'], stageData['item']['coordinate'][Count]['y'], itemKind[kind]))
            Count += 1
        #Set Objects
        self.objects = []
        objKinds = stageData['object']['kind']
        Count = 0
        for kind in objKinds:
            self.objects.append(OBJECT(stageData['object']['coordinate'][Count]['x'], stageData['object']['coordinate'][Count]['y'], objKind[kind], stageData['object']['maketime'][Count]))
            Count += 1


    def contact_check_playerattack_enemy(self):
        if not self.bubbles == [] and self.bubbles[-1].state == self.bubbles[-1].STATE_FLY:
            for enemy in self.enemies:
                if not contact_check_two_object(self.bubbles[-1], enemy):
                    continue
                if enemy.state in (enemy.STATE_DEAD, enemy.STATE_STUCK_GREEN, enemy.STATE_STUCK_YELLOW, enemy.STATE_STUCK_RED,
                enemy.STATE_NONE, enemy.STATE_PON):
                    continue
                if enemy.TYPE not in ('BOSS', "SKULL"):
                    enemy.stuck_by_bubble(self.bubbles[-1].direct)
                    self.bubbles[-1].touch_enemy(enemy.TYPE)
                    break
                elif enemy.TYPE in('BOSS', "SKULL"):
                    self.bubbles[-1].touch_enemy(enemy.TYPE)
                    self.player.earn_score(20)
                    break

    def contact_check_player_enemy(self):
        if self.player.state in (self.player.STATE_DEAD, self.player.STATE_BURN, self.player.STATE_STAGEMOVE):
            return
        for enemy in self.enemies:
            # enemy is alive
            if enemy.state not in (
            enemy.STATE_DEAD, enemy.STATE_STUCK_GREEN, enemy.STATE_STUCK_YELLOW, enemy.STATE_STUCK_RED,
            enemy.STATE_NONE, enemy.STATE_PON):
                if self.player.noDie == False and not self.player.state == self.player.STATE_DEAD and contact_check_two_object(
                        self.player, enemy):
                    self.player.frame = self.player.totalFrame = 0
                    self.player.state = self.player.STATE_DEAD
                    self.playTime = 0.0
                    self.skullAppear = 1
                    for enemy in self.enemies:
                        if not enemy.state == enemy.STATE_WALK:
                            continue
                        if enemy.TYPE == 'SKULL':
                            enemy.frame = enemy.totalFrame = 0
                            enemy.state = enemy.STATE_DEAD
                    self.hurry = False
                    self.player.sounds[2].play()
                    self.player.change_actionPerTime()
            # enemy is stucked
            elif enemy.state == enemy.STATE_STUCK_GREEN or enemy.state == enemy.STATE_STUCK_YELLOW or enemy.state == enemy.STATE_STUCK_RED:
                if contact_check_two_object(self.player, enemy):
                    enemy.direct = random.randint(0, 1)
                    enemy.frame = enemy.totalFrame = 0
                    enemy.state = enemy.STATE_DEAD
                    self.sounds.play()
                    enemy.change_actionPerTime()
                    if enemy.TYPE == 'BOSS':
                        self.player.earn_score(10000)
                        self.musics[3].play()
                    else:
                        self.player.earn_score(100)


    def contact_check_enemyattack_player(self):
        if self.player.state in (self.player.STATE_DEAD, self.player.STATE_BURN, self.player.STATE_STAGEMOVE):
            return
        for attack in self.attacks:
            if not attack.state == attack.STATE_BOOM and not attack.state == attack.STATE_NONE:
                if self.player.noDie == False and not self.player.state == self.player.STATE_DEAD and contact_check_two_object(
                        self.player, attack):
                    self.player.frame = self.player.totalFrame = 0
                    self.player.state = self.player.STATE_DEAD
                    self.player.sounds[2].play()
                    self.playTime = 0.0
                    self.skullAppear = 1
                    for enemy in self.enemies:
                        if not enemy.state == enemy.STATE_WALK:
                            continue
                        if enemy.TYPE == 'SKULL':
                            enemy.frame = enemy.totalFrame = 0
                            enemy.state = enemy.STATE_DEAD
                    self.hurry = False
                    self.player.change_actionPerTime()


    def contact_check_bubble_player(self):
        for bubble in self.bubbles:
            if self.player.state in(self.player.STATE_DEAD, self.player.STATE_BURN, self.player.STATE_STAGEMOVE) or\
                            bubble.state in (bubble.STATE_FLY, bubble.STATE_PON, bubble.STATE_NONE):
                continue
            if contact_check_two_object(bubble, self.player):
                bubble.totalFrame = 0.0
                bubble.direct = self.player.direct
                bubble.state = bubble.STATE_PON
                self.player.earn_score(20)


    def contact_check_stage_player(self):
        for tile in self.stages:
            if not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN \
                    and not self.player.state == self.player.STATE_STAGEMOVE:
                # check left or right tile
                if self.player.jumpPoint == 1:
                    if self.player.get_bb_left() < tile.get_bb_right() and tile.get_bb_left() < self.player.get_bb_right() :
                        continue
                if self.player.state == self.player.STATE_MOVE or self.player.stateTemp == self.player.STATE_MOVE:
                    if self.player.state == self.player.STATE_DOWN:
                        ychecker = self.player.y
                    else:
                        ychecker = self.player.get_bb_bottom()
                    if self.player.direct == self.player.DIRECT_LEFT and not 675 <= tile.y and tile.get_bb_left() < self.player.get_bb_left():
                        if tile.get_bb_bottom() <= ychecker and ychecker < tile.get_bb_top():
                            if tile.get_bb_left() <= self.player.get_bb_left() and self.player.get_bb_left() <= tile.get_bb_right():
                                self.player.x = tile.get_bb_right() + self.player.XSIZE / 2
                                break
                    elif self.player.direct == self.player.DIRECT_RIGHT and not 675 <= tile.y and self.player.get_bb_right() < tile.get_bb_right():
                        if tile.get_bb_bottom() <= ychecker and ychecker < tile.get_bb_top():
                            if tile.get_bb_left() <= self.player.get_bb_right() and self.player.get_bb_right() <= tile.get_bb_right():
                                self.player.x = tile.get_bb_left() - self.player.XSIZE / 2
                                break
        changed = False
        for tile in self.stages:
            if not self.player.state == self.player.STATE_DEAD and not self.player.state == self.player.STATE_BURN \
                    and not self.player.state == self.player.STATE_STAGEMOVE:
                if not self.player.jumpPoint == 1 and tile.y < self.player.bfY - self.player.YSIZE / 2 and not 675 <= tile.y and contact_check_two_object(
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
            if enemy.state in (
                    enemy.STATE_DEAD, enemy.STATE_STUCK_GREEN, enemy.STATE_STUCK_YELLOW, enemy.STATE_STUCK_RED,
                    enemy.STATE_NONE, enemy.STATE_PON):
                continue
            for tile in self.stages:
                # check left or right tile
                if enemy.state == enemy.STATE_JUMP or enemy.state == enemy.STATE_DEAD:
                    if enemy.get_bb_left() < tile.get_bb_right() and tile.get_bb_left() < enemy.get_bb_right():
                        continue
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
                if not enemy.state == enemy.STATE_DEAD:
                    if enemy.state == enemy.STATE_DOWN and tile.y < enemy.bfY - enemy.YSIZE / 2 and not 675<=tile.y and contact_check_two_object(enemy, tile):
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
            if enemy.TYPE in ("WALKER", "MAGICIAN", "BOSS", "SKULL"):
                continue
            if enemy.state in (
                    enemy.STATE_DEAD, enemy.STATE_STUCK_GREEN, enemy.STATE_STUCK_YELLOW, enemy.STATE_STUCK_RED,
                    enemy.STATE_NONE, enemy.STATE_PON):
                continue
            for tile in self.stages:
                # check left or right tile
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
                    if 650 < tile.y and bubble.get_bb_left() < tile.x and tile.x < bubble.get_bb_right() and contact_check_two_object(bubble, tile):
                        bubble.y = tile.get_bb_bottom() - bubble.RADIUS / 2
                        bubble.direct = bubble.directTemp
                        break
                elif bubble.direct == bubble.DIRECT_LEFT:
                    if bubble.state == bubble.STATE_FLY:
                        if contact_check_two_object(bubble, tile):
                            bubble.x = tile.get_bb_right() + bubble.RADIUS / 2
                            bubble.totalFrame = bubble.frame = 0
                            if self.player.attackMode == self.player.ATTACK_NORMAL:
                                bubble.state = bubble.STATE_NORMAL
                            elif self.player.attackMode == self.player.ATTACK_THUNDER:
                                bubble.state = bubble.STATE_THUNDER
                            elif self.player.attackMode == self.player.ATTACK_WATER:
                                bubble.state = bubble.STATE_WATER
                            bubble.direct = bubble.DIRECT_UP
                    else:
                        if bubble.directTemp != bubble.DIRECT_RIGHT and bubble.x - bubble.RADIUS / 2 <= 50:
                            bubble.directTemp = bubble.DIRECT_RIGHT
                            bubble.direct = bubble.DIRECT_UP
                        elif not contact_check_two_object(bubble, tile):
                            bubble.direct = bubble.DIRECT_UP
                elif bubble.direct == bubble.DIRECT_RIGHT:
                    if bubble.state == bubble.STATE_FLY:
                        if contact_check_two_object(bubble, tile):
                            bubble.x = tile.get_bb_left() - bubble.RADIUS / 2
                            bubble.totalFrame = bubble.frame = 0
                            if self.player.attackMode == self.player.ATTACK_NORMAL:
                                bubble.state = bubble.STATE_NORMAL
                            elif self.player.attackMode == self.player.ATTACK_THUNDER:
                                bubble.state = bubble.STATE_THUNDER
                            elif self.player.attackMode == self.player.ATTACK_WATER:
                                bubble.state = bubble.STATE_WATER
                            bubble.direct = bubble.DIRECT_UP
                    else:
                        if bubble.directTemp != bubble.DIRECT_LEFT and 1150 <= bubble.x + bubble.RADIUS / 2:
                            bubble.directTemp = bubble.DIRECT_LEFT
                            bubble.direct = bubble.DIRECT_UP
                        elif not contact_check_two_object(bubble, tile):
                            bubble.direct = bubble.DIRECT_UP


    def contact_check_stage_enemyBubble(self):
        for enemy in self.enemies:
            if enemy.TYPE == 'BOSS':
                continue
            if not enemy.state in (enemy.STATE_STUCK_GREEN, enemy.STATE_STUCK_YELLOW, enemy.STATE_STUCK_RED):
                continue
            for tile in self.stages:
                if enemy.direct == enemy.DIRECT_UP:
                    if 650 < tile.y and enemy.get_bb_left() < tile.x and tile.x < enemy.get_bb_right() and contact_check_two_object(enemy, tile):
                        enemy.y = tile.get_bb_bottom() - enemy.YSIZE / 2
                        enemy.direct = enemy.directTemp
                        break
                elif enemy.direct == enemy.DIRECT_LEFT:
                    if enemy.directTemp != enemy.DIRECT_RIGHT and enemy.x - enemy.XSIZE / 2 <= 50:
                        enemy.directTemp = enemy.DIRECT_RIGHT
                        enemy.direct = enemy.DIRECT_UP
                    elif not contact_check_two_object(enemy, tile):
                        enemy.direct = enemy.DIRECT_UP
                elif enemy.direct == enemy.DIRECT_RIGHT:
                    if enemy.directTemp != enemy.DIRECT_LEFT and 1150 <= enemy.x + enemy.XSIZE / 2:
                        enemy.directTemp = enemy.DIRECT_LEFT
                        enemy.direct = enemy.DIRECT_UP
                    elif not contact_check_two_object(enemy, tile):
                        enemy.direct = enemy.DIRECT_UP


    def contack_check_stage_enemyAttack(self):
        for attack in self.attacks:
            if attack.state in (attack.STATE_BOOM, attack.STATE_NONE) or attack.TYPE == 'BOTTLE':
                continue
            for tile in self.stages:
                if attack.direct == attack.DIRECT_LEFT:
                    if contact_check_two_object(attack, tile):
                        attack.x = tile.get_bb_right() + attack.RADIUS / 2
                        attack.totalFrame = attack.frame = 0
                        attack.state = attack.STATE_BOOM
                        attack.sounds.play()
                elif attack.direct == attack.DIRECT_RIGHT:
                    if contact_check_two_object(attack, tile):
                        attack.x = tile.get_bb_left() - attack.RADIUS / 2
                        attack.totalFrame = attack.frame = 0
                        attack.state = attack.STATE_BOOM
                        attack.sounds.play()


    def contact_check_stage_item(self):
        for item in self.items:
            for tile in self.stages:
                if item.direct == item.DIRECT_DOWN:
                    if tile.y < item.y and item.get_bb_left() < tile.x and tile.x < item.get_bb_right() and contact_check_two_object(item, tile):
                        item.y = tile.get_bb_top() + item.YSIZE / 2
                        item.direct = item.DIRECT_STAY
                        break


    def contact_check_player_item(self):
        if self.player.state in (self.player.STATE_DEAD, self.player.STATE_STAGEMOVE, self.player.STATE_BURN):
            return
        for item in self.items:
            if item.state in(item.STATE_NONE, item.STATE_FONT):
                continue
            if contact_check_two_object(self.player, item):
                item.state = item.STATE_FONT
                item.direct = item.DIRECT_STAY
                item.sounds.play()
                self.player.earn_score(item.score)
                if item.itemNumber == item.KIND_HEALTH:
                    self.player.playerHealth += 1
                elif item.itemNumber == item.KIND_RUN:
                    self.player.currentSpeedKMPH = self.player.MAX_MOVE_SPEED_KMPH
                    self.player.moveSpeedPPS = self.player.change_moveSpeed(self.player.currentSpeedKMPH)
                elif item.itemNumber == item.KIND_LONG:
                    self.player.attackRange = self.player.ATTACK_RANGE_MAX
                elif item.itemNumber == item.KIND_FAST:
                    self.player.currentAttackTerm = self.player.ATTACK_TERM_MIN
                elif item.itemNumber == item.KIND_THUNDER:
                    self.player.attackMode = self.player.ATTACK_THUNDER


    def contact_check_effect_enemy(self):
        for effect in self.effects:
            if effect.state in (effect.STATE_NONE, effect.STATE_THUNDER_POW):
                continue
            for enemy in self.enemies:
                if enemy.state in (
                enemy.STATE_DEAD, enemy.STATE_STUCK_GREEN, enemy.STATE_STUCK_YELLOW, enemy.STATE_STUCK_RED,#
                enemy.STATE_NONE, enemy.STATE_PON):
                    pass
                if enemy.TYPE == 'BOSS':
                    if contact_check_two_object(effect, enemy):
                        if not effect.state == effect.STATE_THUNDER:
                            effect.frame = effect.totalFrame = 0
                            effect.state = effect.STATE_NONE
                            self.player.earn_score(10)
                            break
                        enemy.health -= 1
                        if enemy.state == enemy.STATE_WALK and enemy.health <= 10:
                            enemy.state = enemy.STATE_ANGRY
                        if enemy.health < 0:
                            enemy.frame = enemy.totalFrame = 0
                            enemy.state = enemy.STATE_STUCK_RED
                            enemy.change_actionPerTime()
                        effect.frame = effect.totalFrame = 0
                        effect.state = effect.STATE_THUNDER_POW
                        effect.sounds[0].play()
                else :
                    if contact_check_two_object(effect, enemy):
                        enemy.direct = random.randint(0, 1)
                        enemy.frame = enemy.totalFrame = 0
                        enemy.state = enemy.STATE_DEAD
                        enemy.change_actionPerTime()
                        self.player.earn_score(100)
                        if effect.state == effect.STATE_THUNDER:
                            self.effects.append(EFFECT(enemy.x, enemy.y, EFFECT.STATE_THUNDER_POW, enemy.direct))
                            effect.sounds[0].play()


    def contact_check_stage_effect(self):
        for effect in self.effects:
            if effect.state in (effect.STATE_THUNDER, effect.STATE_THUNDER_POW, effect.STATE_NONE):
                continue
            changed = False
            for tile in self.stages:
                if effect.direct == effect.DIRECT_DOWN:
                    if contact_check_two_object(effect, tile):
                        effect.y = tile.get_bb_top() + effect.SIZE / 2
                        effect.direct = effect.directTemp
                        changed = True
                        break
                else:
                    if effect.directTemp == effect.DIRECT_LEFT:
                        if effect.get_bb_bottom() <= tile.y and tile.get_bb_left() <= effect.x and contact_check_two_object(effect, tile):
                            effect.directTemp = effect.DIRECT_RIGHT
                            effect.direct = effect.DIRECT_DOWN
                            effect.x = tile.get_bb_right() + effect.SIZE
                    elif effect.directTemp == effect.DIRECT_RIGHT:
                        if effect.get_bb_bottom() <= tile.y and effect.x <= tile.get_bb_right() and contact_check_two_object(effect, tile):
                            effect.directTemp = effect.DIRECT_LEFT
                            effect.direct = effect.DIRECT_DOWN
                            effect.x = tile.get_bb_left() - effect.SIZE

                    if(contact_check_two_object(effect, tile)):
                        changed = True

            if changed == False:
                effect.direct = effect.DIRECT_DOWN





def contact_check_two_object(a, b):
    a_left, a_bottom, a_right, a_top = a.get_bb()
    b_left, b_bottom, b_right, b_top = b.get_bb()
    if b_left <= a_right and a_right <= b_right or b_left <= a_left and a_left <= b_right or a_left <= b_right and b_right <= a_right or a_left <= b_left and b_left <= a_right:
        if b_bottom <= a_top and a_top <= b_top or b_bottom <= a_bottom and a_bottom <= b_top or a_bottom <= b_top and b_top <= a_top or a_bottom <= b_bottom and b_bottom <= a_top:
            return True
    return False