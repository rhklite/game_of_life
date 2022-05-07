import numpy as np
import matplotlib.pyplot as plt

import debug_util as db
import random
from datetime import datetime
import os
from copy import deepcopy

class GameBoard:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        # initialize the board with random
        self.board, self.change_list = self.create_random_world()
        self.neighbors =[
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
        ]

    @db.timer
    def step(self):
        new_board = deepcopy(self.board)
        new_change_list = list()
        db.printWarn(f"{len(self.change_list)} cells to update")
        for row, col in self.change_list:
            n_neighbors, neighbors = self.count_neighbors(row, col)
            cell_state = self.board[row][col]
            new_state =self.new_cell_state(cell_state, n_neighbors)
            
            if new_state != cell_state:
                new_board[row][col] = new_state
                new_change_list+=neighbors
                
        self.board = new_board
        self.change_list=set(new_change_list)
         
    def get_neighbors(self, row, col):
        neighbors = []
        for row_increment, col_increment in self.neighbors:
            n_row, n_col = row + row_increment, col + col_increment            
            if self.index_is_inbound(n_row, n_col):
                neighbors.append((n_row, n_col))
        return neighbors
                
                
    def new_cell_state(self, cell_state: int, n_neighbor:int):
        if not cell_state:
            if n_neighbor ==3:
            # for empty cell, it lives if it has 3 neighbors
                return 1
            return 0
        
        if n_neighbor <=1:
            # for cell with 1 or no neighbors, it dies by solitude
            return 0
        elif n_neighbor <=3:
            # for cell with 2 or 3 neighbors, it lives
            return 1
        # cells with 4 or more neighbors dies by over population
        return 0

    def count_neighbors(self, row: int, col: int):
        neighbors = list()
        live_neighbors = 0
        for row_increment, col_increment in self.neighbors:
            n_row, n_col = row + row_increment, col + col_increment            
            if self.index_is_inbound(n_row, n_col):
                live_neighbors += self.board[n_row][n_col]
                neighbors.append((n_row, n_col))

        return live_neighbors, neighbors
    
    def index_is_inbound(self, row: int, col: int) -> bool:
        row_in = row >= 0 and row < self.width
        col_in = col >= 0 and col < self.height
        return all([row_in, col_in])

    def __repr__(self) -> str:
        return f"{self.board}"

    def create_random_world(self):
        board = [[random.choice([0, 1]) for _ in range(self.width)] for _ in range(self.height)]
        update_list = [(i, j) for i in range(self.width) for j in range(self.height)]
        
        return board, update_list
    
    def render(self):
        board = np.array(self.board)
        img = plt.imshow(board, cmap='gray_r')
        plt.pause(0.001)
        plt.draw()
  
        
        
def main():

    np.random.seed(0)

    delay = 0.3
    simulation_iteration = 1000
    game = GameBoard(100, 100)
    folder = f'change_list_{datetime.now()}'
    os.makedirs('image/'+folder)
    for i in range(simulation_iteration):
        game.render()
        game.step()
        # plt.savefig(f"image/{folder}/{i}.png")


if __name__ == '__main__':
    main()
