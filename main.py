import board
import gui


def main():
    
    ratio = [16, 9]
    multiplier = 10
    width, height = multiplier*ratio[0], multiplier*ratio[1]
    game = board.GameBoardHash(width, height, {n:0 for n in range(width*height)})
    simulator = gui.PygameGUI(game, width=width, height=height, cellsize=14)   
    simulator.run()    

if __name__ == '__main__':
    main()
