import pygame
from pygame.locals import *


class Slideshow:

    def __init__(self, controller):

        self.controller = controller

        self.slides = [pygame.image.load("src/resources/slide1.png").convert(),
                       pygame.image.load("src/resources/slide2.png").convert()]

        self.current_slide = 0

        self.image = self.slides[self.current_slide]

    def next_slide(self):

        self.current_slide += 1
        self.image = self.slides[self.current_slide]
        self.controller.sound_engine.queue_sound(("button_click", 0))
        self.controller.sound_engine.play_sounds()

    def run(self):
        game_exit = False
        continue_to_game = False
        while not (game_exit or continue_to_game):
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.current_slide+1 == len(self.slides):
                            continue_to_game = True
                        else:
                            self.next_slide()

            self.controller.display.blit(self.image, (0, 0))
            pygame.display.flip()
            self.controller.clock.tick(60)

        return game_exit
