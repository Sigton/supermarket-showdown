import pygame

from src import constants


class SpriteSheet(object):

    sprite_sheet = None

    def __init__(self, filename):

        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):

        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(constants.WHITE)

        return image
