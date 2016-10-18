from pico2d import *


class WARP:
    warp = None
    WARP_XSIZE_MAX, WARP_YSIZE_MAX = 100000, 100000
    def __init__(self):
        if WARP.warp == None:
            WARP.warp = load_image('sprite\\surround\\warp.png')
        self.warping = False
        self.warpTime = 0.0
        self.warpXSize, self.warpYSize = 1500, 1500


    def draw(self):
        if self.warping == True:
            self.warp.draw(600, 400, self.warpXSize, self.warpYSize)


    def update(self):
        if self.warping == True:
            self.warpXSize += 1500
            self.warpYSize += 1500
            self.warpTime += 0.05
            if self.WARP_XSIZE_MAX <= self.warpXSize and self.WARP_YSIZE_MAX <= self.warpYSize:
                self.warpXSize, self.warpYSize = 1500, 1500
                self.warpTime = 0
                self.warping = False