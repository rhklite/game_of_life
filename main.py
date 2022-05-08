import os
from datetime import datetime
import numpy as np

import board
import render

from tool import debug_util as db



def main():

    np.random.seed(0)

    delay = 0.3
    simulation_iteration = 1000
    game = board.GameBoardHash(10, 10)
    display = render.MatplotlibRenderer()
    folder = f'change_list_{datetime.now()}'
    os.makedirs('image/' + folder)
    # len(game)
    for i in range(simulation_iteration):
        display(game.get_board())
        game.step()
        plt.savefig(f"image/{folder}/{i}.png")


if __name__ == '__main__':
    main()
