import pygame


class Marker:

    def __init__(self, x, y, tile_x, tile_y):

        self.x = x+4
        self.y = y

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.image = pygame.Surface([40, 24])
        self.image.set_colorkey((0,0,0))
        self.image.set_alpha(127)
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image, (0, 255, 0), self.rect)
        self.rect.topleft = (x+4, y)

        self.active = True

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def draw(self, display):
        if self.active:
            display.blit(self.image, self.rect.topleft)
