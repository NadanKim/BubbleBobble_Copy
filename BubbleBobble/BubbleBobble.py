import game_framework
from pico2d import *

import start_state
import ranking_state

# fill here
open_canvas(1200, 800, True)
#game_framework.run(start_state)
game_framework.run(ranking_state)
close_canvas()