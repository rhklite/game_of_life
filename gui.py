import os
from datetime import datetime
import time

import pygame
import numpy as np
import matplotlib.pyplot as plt

from typing import Sequence

from tool import debug_util as db


class MatplotlibRenderer:
    def __init__(
        self, game, save=False, save_path='image/', *args, **kwargs
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
        board = np.transpose(np.array(board), (1, 0))
        plt.imshow(board, cmap='gray_r')
        plt.pause(0.001)
        plt.draw()
        if self.save:
            plt.savefig(f"{self.save_path}/{self.iterations}.png")
            self.iterations += 1


class Color:
    alive = (128, 189, 38)
    grid = (30, 30, 60)
    background = (10, 10, 40)
    about_to_die = (200, 200, 225)


class PygameRenderer:
    def __init__(
        self,
        game,
        width,
        height,
        cellsize=8,
        caption="John Conway's Game of Life, Implemented by Han Hu",
        *args,
        **kwargs,
    ) -> None:
        self.cellsize = cellsize
        self.game = game

        pygame.init()
        self.window = pygame.display.set_mode(
            (width * cellsize, height * cellsize)
        )
        pygame.display.set_caption(caption)
        self.window.fill(Color.grid)
        
        self.pause = False
        self.space_bar_pressed = False
        
    def view(self):
        board = self.game.get_board()
        for col_idx, column in enumerate(board):
            for row_idx, state in enumerate(column):
                color = Color.background
                if state == 1:
                    color = Color.alive
                    # color = (255, 255/(j+1), 255/(i+1))
                pygame.draw.rect(
                    self.window,
                    color,
                    (
                        row_idx * self.cellsize,
                        col_idx * self.cellsize,
                        self.cellsize - 1,
                        self.cellsize - 1,
                    ),
                )
        pygame.display.update()

    def update_view(self, row, col):
        new_rectangle = pygame.Rect(row*self.cellsize,
                          col*self.cellsize,
                          self.cellsize-1,
                          self.cellsize-1)
                          
        pygame.draw.rect(self.window, Color.alive, new_rectangle)
        pygame.display.update(new_rectangle)
        
    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.space_bar_pressed = not self.space_bar_pressed
                        self.pause = self.space_bar_pressed
                        
                if pygame.mouse.get_pressed()[0]:
                    # self.pause = True
                    try:
                        mouse_position = event.pos
                        cell_row = mouse_position[0] // self.cellsize
                        cell_col = mouse_position[1] // self.cellsize
                        self.game.set_cell(cell_row, cell_col)
                        self.update_view(cell_row, cell_col)
                    except AttributeError:
                        pass
                
                # if event.type == pygame.MOUSEBUTTONUP:
                #     self.pause = False
                
                
                # if self.space_bar_pressed:
                #     self.pause = True 
                
            if not self.pause:    
                self.view()
                self.game.step()
                