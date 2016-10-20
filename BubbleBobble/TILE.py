from pico2d import *

class TILE:
    bigTile = None
    smallTile = None
    def __init__(self, tileNumber, tileX, tileY):
        self.tileNumber = tileNumber
        self.stageSize = 25
        self.tileSize = 12.5
        if TILE.bigTile == None:
            TILE.bigTile = load_image('sprite\\MapTile\\BIGTILE.png')
        if TILE.smallTile == None:
            TILE.smallTile = load_image('sprite\\MapTile\\SMALLTILE.png')

        if 0 < tileNumber and tileNumber <= 100:
            self.left = (tileNumber - 1) % 10 * self.stageSize * 2
            self.bottom = int(9 - (tileNumber - tileNumber % 10) / 10) * self.stageSize * 2
            self.size = self.stageSize * 2
            self.x = self.tileSize * 2 + tileX * self.stageSize
            self.y = self.tileSize * 2 + tileY * self.stageSize
        elif 100 < tileNumber and tileNumber <=200:
            self.left = (tileNumber - 101) % 10 * self.stageSize
            self.bottom = int(9 - ((tileNumber-100) - (tileNumber-100) % 10) / 10) * self.stageSize
            self.size = self.stageSize
            self.x = self.tileSize + tileX * self.stageSize
            self.y = self.tileSize + tileY * self.stageSize


    def get_bb(self):
        if 0 < self.tileNumber and self.tileNumber <= 100:
            return self.x - self.tileSize * 2, self.y - self.tileSize * 2, self.x + self.tileSize * 2, self.y + self.tileSize * 2
        elif 100 < self.tileNumber and self.tileNumber <= 200:
            return self.x - self.tileSize, self.y - self.tileSize, self.x + self.tileSize, self.y + self.tileSize


    def get_bb_y(self):
        if 0 < self.tileNumber and self.tileNumber <= 100:
            return self.y + self.tileSize * 2
        elif 100 < self.tileNumber and self.tileNumber <= 200:
            return self.y + self.tileSize

    def draw_bb(self):
        draw_rectangle(*self.get_bb())



    def draw(self):
        if 0 < self.tileNumber and self.tileNumber <= 100:
            self.bigTile.clip_draw(self.left, self.bottom, self.size, self.size, self.x, self.y)
        elif 100 < self.tileNumber and self.tileNumber <= 200:
            self.smallTile.clip_draw(self.left, self.bottom, self.size, self.size, self.x, self.y)