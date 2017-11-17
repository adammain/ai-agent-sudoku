import pygame

from pygame import *


class SudokuSquare:
    """A sudoku square class."""

    def __init__(self, number=None, offsetX=0, offsetY=0, edit="Y", xLoc=0, yLoc=0):
        if number != None:
            number = str(number)
            self.color = (2, 204, 186)
        else:
            number = ""
            self.color = (255, 255, 255)
        # print("FONTS", pygame.font.get_fonts())
        self.font = pygame.font.SysFont('opensans', 21)
        self.text = self.font.render(number, 1, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos = self.textpos.move(offsetX + 17, offsetY + 4)

        # self.collide = pygame.Surface((25, 22))
        # self.collide = self.collide.convert()
        # AAfilledRoundedRect(pygame.display.get_surface(), (xLoc, yLoc, 25, 22), (255, 255, 255))
        # self.collide.fill((2, 204, 186))
        # self.collideRect = self.collide.get_rect()
        # self.collideRect = self.collideRect.move(offsetX + 1, offsetY + 1)
        # The rect around the text is 11 x 28

        self.edit = edit
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.offsetX = offsetX
        self.offsetY = offsetY

    def draw(self):
        screen = pygame.display.get_surface()
        AAfilledRoundedRect(
            screen, (self.offsetX, self.offsetY, 45, 40), self.color)

        # screen.blit(self.collide, self.collideRect)
        screen.blit(self.text, self.textpos)

    def checkCollide(self, collision):
        if len(collision) == 2:
            return self.collideRect.collidepoint(collision)
        elif len(collision) == 4:
            return self.collideRect.colliderect(collision)
        else:
            return False

    def highlight(self):
        self.collide.fill((190, 190, 255))
        self.draw()

    def unhighlight(self):
        self.collide.fill((255, 255, 255, 255))
        self.draw()

    def change(self, number):
        if number != None:
            number = str(number)
        else:
            number = ""

        if self.edit == "Y":
            self.text = self.font.render(number, 1, (0, 0, 0))
            self.draw()
            return 0
        else:
            return 1

    def currentLoc(self):
        return self.xLoc, self.yLoc
