from __future__ import annotations

import abc
import copy
import random


class BaseBoard(abc.ABC):
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.board = None

    def __repr__(self) -> str:
        return f"{self.board}"

    def new_cell_state(self, cell_state: int, n_neighbor: int):
        if not cell_state:
            if n_neighbor == 3:
                # for empty cell, it lives if it has 3 neighbors
                return 1
            return 0

        if n_neighbor <= 1:
            # for cell with 1 or no neighbors, it dies by solitude
            return 0
        elif n_neighbor <= 3:
            # for cell with 2 or 3 neighbors, it lives
            return 1
        # cells with 4 or more neighbors dies by over population
        return 0

    def __len__(self):
        return self.width * self.height

    
    def view(self):
        print(self.get_board())
    
    @property
    def dim(self):
        return (self.width, self.height)

    @abc.abstractmethod
    def step(self):
        pass

    @abc.abstractmethod
    def get_board(self):
        pass

    @abc.abstractmethod
    def set_cell(self):
        pass

class GameBoardHash(BaseBoard):
    """uses dictionary to precompute all the neighbors indices rather than computing it live.
    ~60fps at 100x100
    """
    def __init__(self, width: int, height: int, board = None) -> None:
        super().__init__(width, height)
        
        
        self.board, self.update_list = self.create_random_1d_world()
        if board is not None:
            self.board = board

        self.next_to_die = list()
        self.updated_cell = self.board
        
        self.neighbors_map = {
            idx: self.compute_neighbors(idx) for idx in range(len(self))
        }


    # @db.timer
    def step(self):
        old_board = copy.deepcopy(self.board)
        
        new_update_list = list()
        next_to_die = list()
        updated_cell = list()
        for idx in self.update_list:
            cell_state = old_board[idx]
            n_neighbors, neighbors = self.count_neighbors(idx, old_board)            
            new_state = self.new_cell_state(cell_state, n_neighbors)
            if new_state != cell_state:
                self.board[idx] = new_state
                new_update_list +=neighbors
                updated_cell.append(idx)
                if new_state == 0:
                    next_to_die.append(idx)

        self.update_list = set(new_update_list)
        self.next_to_die = next_to_die   
        self.updated_cell = updated_cell
        
    def count_neighbors(self, idx, board):
        neighbors = self.neighbors_map[idx]
        live_neighbors = 0
        for n in neighbors:
            live_neighbors += board[n]
            
        return live_neighbors, neighbors    

    def create_random_1d_world(self):

        board = {idx: random.choice([0, 1]) for idx in range(len(self))}
        update_list = {i for i in range(len(self))}
        return board, update_list

    def compute_neighbors(self, idx):

        neighbors = list()
        idx_row = idx // self.width
        top_idx = idx - self.width
        if top_idx >= 0 and top_idx // self.width == idx_row - 1:
            neighbors.append(top_idx)
        # bottom
        bottom_idx = idx + self.width
        if bottom_idx < len(self) and bottom_idx // self.width == idx_row + 1:
            neighbors.append(bottom_idx)
        # left
        left_idx = idx - 1
        if left_idx >= 0 and left_idx // self.width == idx_row:
            neighbors.append(left_idx)
        # right
        right_idx = idx + 1
        if right_idx < len(self) and right_idx // self.width == idx_row:
            neighbors.append(right_idx)

        # top_left
        top_left_idx = idx - 1 - self.width
        if top_left_idx >= 0 and top_left_idx // self.width == idx_row - 1:
            neighbors.append(top_left_idx)

        # top right
        top_right_idx = idx + 1 - self.width
        if top_right_idx >= 0 and top_right_idx // self.width == idx_row - 1:
            neighbors.append(top_right_idx)

        # bottom_left
        bottom_left_idx = idx - 1 + self.width
        if (
            bottom_left_idx < len(self)
            and bottom_left_idx // self.width == idx_row + 1
        ):
            neighbors.append(bottom_left_idx)

        # bottom_right
        bottom_right_idx = idx + 1 + self.width
        if (
            bottom_right_idx < len(self)
            and bottom_right_idx // self.width == idx_row + 1
        ):
            neighbors.append(bottom_right_idx)

        return neighbors

    def get_board(self):
        board = [state for state in self.board.values()]
        return np.array(board).reshape(self.height, self.width)

    def get_updated_cell(self):
        return [self.flat_to_2d(cell) for cell in self.updated_cell]
    
    def set_cell(self, row, col):
        cell_idx = self.coord_to_1d(row, col)

        self.board[cell_idx] = 1
        neighbors = self.neighbors_map[cell_idx]
        
        to_update = neighbors + [cell_idx]
        self.update_list = self.update_list.union(set(to_update))
        
    def coord_to_1d(self, row_idx, col_idx):
        return col_idx*self.width + row_idx
    
    def flat_to_2d(self, idx):
        return idx%self.width, idx//self.width

    def get_next_to_die(self):
        return [self.flat_to_2d(cell) for cell in self.next_to_die]
    