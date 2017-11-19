import sys
import os
import random
import pygame
sys.path.append(os.path.join("objects"))
import SudokuSquare
from GameResources import *

digits = '123456789'
rows = 'ABCDEFGHI'


def play(values_list):
    pygame.init()

    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    background_image = pygame.image.load(
        "./images/sudoku-board-bare.jpg").convert()

    clock = pygame.time.Clock()

if __name__ == "__main__":
    main()
    sys.exit()
