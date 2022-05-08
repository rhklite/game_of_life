import os
from datetime import datetime
import numpy as np
import time

import board
import gui

from tool import debug_util as db



def main():

    width, height = 16*14, 9*14
    game = board.GameBoardHash(width, height, {n:0 for n in range(width*height)})
    

    simulator = gui.PygameRenderer(game, width=width, height=height, cellsize=10, save=True)
    # while True:
    #     simulator.view()
    
    simulator.run()    

if __name__ == '__main__':
    main()
