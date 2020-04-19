import pygame

from src import spritesheet, gui_components, catalogue, constants


class HUD:

    def __init__(self):

        self.weekdays = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

        ss = spritesheet.SpriteSheet("src/resources/hud.png")

        self.hud_background = ss.get_image(0, 0, 960, 720)
        self.hud_background_rect = self.hud_background.get_rect()

        self.day_number = gui_components.Label(495, 48, "Day 1: Mon", True, 48, (227, 238, 192))

        self.day_progress = gui_components.ProgressBar(753, 24, 100, 8, ((32, 32, 32), (174, 186, 137)))

        self.money_label = gui_components.Label(42, 5, "Money: $500", False, 32, (227, 238, 192))
        self.salary_label = gui_components.Label(42, 44, "Salary: $80/hr", False, 32, (227, 238, 192))
        self.lives_label = gui_components.Label(691, 44, "Lives left: 3", False, 32, (227, 238, 192))

        self.cat_man = catalogue.CatalogueManager(0, 140)

        self.daily_bonus = DailyBonus(450, -122)
        self.game_over = GameOver(330, -155)

    def update(self, money, salary, day, hour, lives):

        self.day_number.update("Day {}: {}".format(day, self.weekdays[(day-1) % 7]))
        self.day_progress.update(hour/12)
        self.money_label.update("Money: ${}".format(money))
        self.salary_label.update("Salary: ${}/hr".format(salary))
        self.lives_label.update("Lives left: {}".format(lives))

        self.cat_man.update(money)
        self.daily_bonus.update()
        self.game_over.update()

    def draw(self, display):

        display.blit(self.hud_background, self.hud_background_rect.topleft)
        self.day_progress.draw(display)
        self.day_number.draw(display)
        self.money_label.draw(display)
        self.salary_label.draw(display)
        self.lives_label.draw(display)

        self.cat_man.draw(display)
        self.daily_bonus.draw(display)
        self.game_over.draw(display)


class DailyBonus:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.image = pygame.image.load("src/resources/daily_bonus.png").convert()
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.timer = 0
        self.move_speed = 10
        self.move = 0

    def begin_move_in(self):
        self.y = -122
        self.timer = 43
        self.move = self.move_speed

    def begin_move_out(self):
        self.y = 308
        self.timer = 43
        self.move = -self.move_speed

    def update(self):

        if self.move != 0:
            if self.timer >= 0:
                self.timer -= 1
                self.y += self.move
            else:
                self.move = 0

        self.rect.topleft = (self.x, self.y)

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)


class GameOver:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.image = pygame.image.load("src/resources/game_over.png").convert()
        self.image.set_colorkey(constants.WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.timer = 0
        self.move_speed = 10
        self.move = 0

    def begin_move_in(self):
        self.y = -115
        self.timer = 47
        self.move = self.move_speed

    def begin_move_out(self):
        self.y = 315
        self.timer = 47
        self.move = -self.move_speed

    def update(self):

        if self.move != 0:
            if self.timer >= 0:
                self.timer -= 1
                self.y += self.move
            else:
                self.move = 0

        self.rect.topleft = (self.x, self.y)

    def draw(self, display):
        display.blit(self.image, self.rect.topleft)
