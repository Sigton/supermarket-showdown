import pygame

from src import constants


class Tile:

    def __init__(self, x, y, image):

        self.x = x
        self.y = y

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)
