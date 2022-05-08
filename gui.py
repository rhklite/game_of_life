import pygame
from tool import debug_util as db


class Color:
    alive = (128, 189, 38)
    grid = (30, 30, 60, 0)
    background = (10, 10, 40)
    next_to_die = (58, 125, 22)


class PygameGUI:
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
        self.max_size = cellsize
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
        about_to_die = self.game.get_next_to_die()

        for col_idx, column in enumerate(board):
            for row_idx, state in enumerate(column):

                color = Color.background
                if state == 1:
                    color = Color.alive

                if (row_idx, col_idx) in about_to_die:
                    color = Color.next_to_die

                cell = (
                    row_idx * self.cellsize,
                    col_idx * self.cellsize,
                    self.cellsize - 1,
                    self.cellsize - 1,
                )
                pygame.draw.rect(self.window, color, cell)
        pygame.display.update()

    def update_view(self, row, col):
        new_rectangle = pygame.Rect(
            row * self.cellsize,
            col * self.cellsize,
            self.cellsize - 1,
            self.cellsize - 1,
        )

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

                    if event.key == pygame.K_RIGHT:
                        self.view()
                        self.game.step()

                if pygame.mouse.get_pressed()[0]:
                    try:
                        mouse_position = event.pos
                        cell_row = mouse_position[0] // self.cellsize
                        cell_col = mouse_position[1] // self.cellsize
                        self.game.set_cell(cell_row, cell_col)
                        self.update_view(cell_row, cell_col)
                    except AttributeError:
                        pass

            if not self.pause:
                self.view()
                self.game.step()

