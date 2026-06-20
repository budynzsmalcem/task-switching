from psychopy import visual, core
from psychopy.hardware import keyboard

import bodzce1feedback import *
_config_defaults = load_config()

if __name__ == "__main__":
    trial(_config_defaults[""])
    win.close()
    core.quit()
