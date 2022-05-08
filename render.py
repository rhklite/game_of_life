import os
from datetime import datetime

import pygame
import numpy as np
import matplotlib.pyplot as plt

from typing import Sequence


class MatplotlibRenderer:
    def __init__(
        self, save=False, save_path='image/', *args, **kwargs
    ) -> None:
        self.seq_counter = 0
        self.save_path = save_path
        self.save = save
        self.iterations = 0

        if self.save:
            folder = f'change_list_{datetime.now()}'
            self.save_path = os.path.join(self.save_path, folder)
            os.makedirs(self.save_path)

    def view(self, board: Sequence) -> None:
        board = np.array(board)
        plt.imshow(board, cmap='gray_r')
        plt.pause(0.001)
        plt.draw()
        if self.save:
            plt.savefig(f"{self.save_path}/{self.iterations}.png")
            self.iterations += 1


class PygameRenderer:
    def __init__(
        self,
        width,
        height,
        cellsize=8,
        caption="John Conway's Game of Life, Implemented by Han Hu",
        *args,
        **kwargs,
    ) -> None:
        self.cellsize = cellsize
        
        self.background = (10, 10, 40)
        self.grid_color = (30, 30, 60)
        self.alive_color = (200, 200, 225)
        
        pygame.init()
        self.window = pygame.display.set_mode(
            (width * cellsize, height * cellsize)
        )
        pygame.display.set_caption(caption)
        self.window.fill(self.grid_color)
        
    def view(self, board: Sequence):

        for i, row in enumerate(board):
            for j, col in enumerate(row):
                color = self.background
                if col == 1:
                    color = self.alive_color
                pygame.draw.rect(
                    self.window,
                    color,
                    (
                        i * self.cellsize,
                        j * self.cellsize,
                        self.cellsize - 1,
                        self.cellsize - 1,
                    ),
                )
        pygame.display.update()
