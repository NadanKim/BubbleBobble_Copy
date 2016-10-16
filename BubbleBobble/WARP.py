from pico2d import *


class WARP:
    warp = None
    WARP_XSIZE_MAX, WARP_YSIZE_MAX = 15000, 15000
    def __init__(self):
        self.currentStage = 0
        if WARP.warp == None:
            WARP.warp = load_image('sprite\\surround\\warp.png')
        self.warping = True
        self.warpXSize, self.warpYSize = 0, 0


    def draw(self):
        if self.warping == True:
            self.warp.draw(600, 400, self.warpXSize, self.warpYSize)


    def update(self):
        if self.warping == True:
            self.warpXSize += 180
            self.warpYSize += 180
            if self.WARP_XSIZE_MAX <= self.warpXSize and self.WARP_YSIZE_MAX <= self.warpYSize:
                self.warping = False