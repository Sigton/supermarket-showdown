from src import spritesheet

# format: price
barrier_data = {"Barrier": [50]}


class Barrier:

    def __init__(self, x, y, tile_x, tile_y):

        self.x = x
        self.y = y

        self.tile_x = tile_x
        self.tile_y = tile_y

        ss = spritesheet.SpriteSheet("src/resources/turrets.png")

        self.image = ss.get_image(0, 48, 48, 48)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)
