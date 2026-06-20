import os
import pandas as pd
from psychopy import visual, core
from psychopy.hardware import keyboard
import random
import functions import *

global_trial_number = 0
answered = False
correct_answer = False
rt = None
response_key = None

if __name__ == "__main__":
    trial()
    win.close()
    core.quit()
