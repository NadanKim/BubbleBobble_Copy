from pico2d import *
from BUBBLE import BUBBLE



class OBJECT:
    MAKETIME = 2.5
    NORMAL, THUNDER, WATER, FIRE = 0, 1, 2, 3
    DIRECT_UP = 2
    def __init__(self, x, y, kind=NORMAL, makeTime=2.5):
        self.x, self.y = x, y
        self.kind = kind
        self.rewindTime = 0.0
        self.MAKETIME = makeTime


    def update(self, frameTime):
        self.rewindTime += frameTime
        if self.MAKETIME < self.rewindTime:
            self.rewindTime = 0.0
            return BUBBLE(self.x, -BUBBLE.RADIUS, self.DIRECT_UP, 0, self.kind)