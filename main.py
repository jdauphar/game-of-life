"""
1. The immediate neighbors of a cell are those cells occupying the eight horizontally,
vertically, and diagonally adjacent cells.
2. If a LIFE cell has fewer than two immediate neighbors, it dies of loneliness. If a LIFE
cell has more than three immediate neighbors, it dies of overcrowding.
3. If an empty square has exactly three LIFE cells as immediate neighbors, a new cell is
born in the square.
4. Births and deaths all take place exactly at the change of generations. Thus a dying cell
may help birth a new one, but a newborn cell may not resurrect a dying cell, nor may one
dying cell stave off death for another by lowering the local population density.
"""
import random
from PIL import Image

def fill_board_randomly(board, l, w):
    for x in range(0, l):
        for y in range(0, w):
            board[x][y] = random.choice([0, 1])
    return board

def generation(old_board):
    new_board = [[0 for x in range(w)]for y in range(l)]
    for x in range(0, l):
        for y in range(0, w):
            neighbors = count_neighbors(old_board, x, y)
            if neighbors < 2:
                new_board[x][y] = 0
            elif neighbors > 3:
                new_board[x][y] = 0
            else:
                new_board[x][y] = 1
    return new_board


def count_neighbors(gen, x, y):
    count = 0
    at_xmax = 1 - (x == (l - 1))
    at_ymax = 1 - (y == (w - 1))
    at_xmin = 1 - (x == 0)
    at_ymin = 1 - (y == 0)
    # this checks in a grid around the cell like minesweeper
    count = (((gen[x - 1*at_xmin][y - 1*at_ymin]) * at_xmin * at_ymin) + (gen[x][y - 1*at_ymin] * at_ymin ) + (gen[x + 1*at_xmax][y - 1*at_ymin] * at_xmax * at_ymin) +
             (gen[x - 1*at_xmin][y] * at_xmin) + (gen[x][y] * 0) + (gen[x + 1*at_xmax][y]) * at_xmax +
             (gen[x - 1*at_xmin][y + 1*at_ymax] * at_xmin * at_ymax) + (gen[x][y + 1*at_ymax] * at_ymax) + (gen[x + 1*at_xmax][y + 1*at_ymax] * at_xmax * at_ymax))

    return count

def save_images(history, l, w):
    count = 1
    for generation in history:
        img = Image.new("RGB", (l, w), "white")
        pixels = img.load()  # Create the pixel map
        for i in range(img.size[0]):  # For every pixel:
            for j in range(img.size[1]):
                pixels[i, j] = "white" if generation[i][j] == 1 else "black" # Set the colour accordingly
        filename = r'.\saves\gen' + str(count) + r'.png'
        count+=1
        img.save(filename)

def make_gif(history, l, w):
    images = []
    for generation in history:
        img = Image.new("RGB", (l, w), "white")
        pixels = img.load()  # Create the pixel map
        for i in range(img.size[0]):  # For every pixel:
            for j in range(img.size[1]):
                pixels[i, j] = (0,0,0) if generation[i][j] == 1 else (255,255,255)  # Set the colour accordingly
        img = img.resize((l*20,w*20))
        images.append(img)
    filename = r'.\saves\after' + str(len(history)) + r'.gif'
    images[0].save(fp=filename, format='GIF', append_images=images[1:],
             save_all=True, duration=200, loop=0)


l = 50
w = 50
generations = 50

board = [[0 for x in range(w)]for y in range(l)]
board = fill_board_randomly(board, l, w)

if __name__ == '__main__':
    count = 1
    history = []
    while count <= generations:
        history.append(board)
        board = generation(board)
        count+=1
    #save_images(history, l, w)
    make_gif(history, l, w)
