import board
import gui


def main():

    width, height = 16*10, 9*10
    game = board.GameBoardHash(width, height, {n:0 for n in range(width*height)})
    simulator = gui.PygameRenderer(game, width=width, height=height, cellsize=14, save=True)   
    simulator.run()    

if __name__ == '__main__':
    main()
