import pygame

from src import constants


class ProgressBar:

    def __init__(self, x, y, length, width, colors):

        self.back_color = colors[0]
        self.fill_color = colors[1]

        self.width = width
        self.length = length

        self.start_image = pygame.Surface([length, width]).convert()
        self.new_image = None

        pygame.draw.line(self.start_image, self.back_color, (0, width//2), (length, width//2), width)

        self.image = self.start_image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y - width//2

    def update(self, percent):

        if percent == 0:
            self.image = self.start_image
            return

        self.new_image = self.start_image.copy()

        pygame.draw.line(self.new_image, self.fill_color, (0, self.width//2),
                         (self.length * percent, self.width//2), self.width)
        self.image = self.new_image

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class Label:

    def __init__(self, x, y, text, center=False, text_size = 32, color=constants.WHITE):

        self.color = color
        self.text_size = text_size

        self.image = constants.load_font(self.text_size).render(text, False, self.color)
        self.rect = self.image.get_rect()

        if center:
            self.rect.center = (x,y)
        else:
            self.rect.topleft = (x,y)

    def update(self, text):

        old_pos = self.rect.topleft

        self.image = constants.load_font(self.text_size).render(text, False, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = old_pos

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class Fill:

    def __init__(self, x, y, width, height, color):

        self.color = color

        self.image = pygame.Surface([width, height]).convert()
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def resize(self, width, height):

        old_pos = self.rect.topleft

        self.image = pygame.Surface([width, height]).convert()
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.topleft = old_pos

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))


class Tooltip:

    def __init__(self, text, x, y, size, colour, direction):

        self.text = Label(x+10, y+4, text, False, size, colour)
        self.background = Fill(x, y, self.text.rect.width + 20, self.text.rect.height + 12, (32, 32, 32))
        self.background_fill = Fill(x, y, self.text.rect.width+16, self.text.rect.height+8, (227, 238, 192))

        self.direction = direction

        self.x = x if self.direction == "R" else x-self.background.rect.width
        self.y = y

        self.components = [
            self.background,
            self.background_fill,
            self.text
        ]

        self.on = False

    def update(self):
        pass

    def reposition(self, pos):
        self.x = pos[0] if self.direction == "R" else pos[0]-self.background.rect.width
        self.y = pos[1]

        self.background.rect.topleft = (self.x, self.y)
        self.background_fill.rect.topleft = (self.x+2, self.y+2)
        self.text.rect.topleft = (self.x+10, self.y+4)

    def draw(self, display):

        if self.on:
            [component.draw(display) for component in self.components]

    def set_on(self):
        self.on = True

    def set_off(self):
        self.on = False
