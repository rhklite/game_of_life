import os
from datetime import datetime
import numpy as np

import board
import render

from tool import debug_util as db



def main():

    np.random.seed(0)
    width, height = 100, 100
    simulation_iteration = 1000
    game = board.GameBoardHash(width, height)
    display = render.PygameRenderer(width=width, height=height, save=True)
    
    for i in range(simulation_iteration):
        display.view(game.get_board())
        game.step()
        


if __name__ == '__main__':
    main()
