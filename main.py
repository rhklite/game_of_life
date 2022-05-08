import os
from datetime import datetime
import numpy as np
import time

import board
import render

from tool import debug_util as db



def main():

    # np.random.seed(0)
    width, height = 160, 90
    simulation_iteration = 1000
    game = board.GameBoardHash(width, height)
    display = render.PygameRenderer(width=width, height=height, cellsize=10, save=True)
    
    while True:
        display.view(game.get_board())
        # game.view()
        game.step()
        # time.sleep(1)
        

if __name__ == '__main__':
    main()
