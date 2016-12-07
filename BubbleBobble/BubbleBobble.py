import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"

import game_framework
from pico2d import *

import start_state

# fill here
open_canvas(1200, 800, True)
game_framework.run(start_state)
close_canvas()