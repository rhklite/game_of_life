import matplotlib.pyplot as plt
import numpy as np

from typing import Sequence

class MatplotlibRenderer:
    def __call__(self, board: Sequence) -> None:
        board = np.array(board)
        plt.imshow(board, cmap='gray_r')
        plt.pause(0.001)
        plt.draw()


