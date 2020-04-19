import pygame

from src import spritesheet, projectiles

import math

# turret data format: shoot freq, sight distance, projectile ref, cost, refill
turret_data = {
    "Cabbage Cannon": [150, 175, projectiles.Cabbage, 200],
    "Juice Rocket": [350, 350, projectiles.Rocket, 600],
    "Glue Gun": [250, 125, projectiles.Glue, 300]
}


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Turret:

    def __init__(self, x, y, tile_x, tile_y, bc, shoot_freq, sight_distance, projectile):

        self.x = x
        self.y = y

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.board_controller = bc

        self.turret_bottom = None
        self.turret_top_image = None
        self.turret_top = None

        self.rect_top = None
        self.rect_bottom = None

        self.target = None
        self.projectile = projectile

        self.sight_distance = sight_distance
        self.shoot_freq = shoot_freq
        self.shoot_timer = 0

    def update(self):

        # we need a target
        if self.target is None:
            self.find_nearest_target()

            # if we failed to find a new target
            # we do not need to attack it
            if self.target is None:
                return
        else:
            # previous target has died and we need to try find a new one
            if self.target.hp <= 0:
                self.target = None
                self.find_nearest_target()

                # if we failed to find a new target
                # we do not need to attack it
                if self.target is None:
                    return

        # check target is in range
        if self.sqr_dist_to_target(self.target) < self.sight_distance * self.sight_distance:
            # we then need to point at the target
            a = self.angle_to_target(self.target) - 90
            self.turret_top = pygame.transform.rotate(self.turret_top_image, a)
            self.rect_top = self.turret_top.get_rect(center=self.rect_top.center)

            # we need to periodically shoot the target
            if self.shoot_timer == 0:
                self.board_controller.projectiles.append(
                    self.projectile(self.rect_top.centerx, self.rect_top.centery, self.target))
                self.shoot_timer = int(self.shoot_freq / self.board_controller.freq_mul)

                self.board_controller.controller.sound_engine.queue_sound(("projectile_fire", 0))
                self.on_shoot()
            else:
                self.shoot_timer -= 1
        else:
            self.target = None

    def find_nearest_target(self):

        min_distance = math.inf
        for customer in self.board_controller.customers:
            d = self.sqr_dist_to_target(customer)
            if d < min_distance:
                self.target = customer
                min_distance = d

    def sqr_dist_to_target(self, t):
        dx = t.x - self.x
        dy = t.y - self.y
        return dx * dx + dy * dy

    def angle_to_target(self, t):
        dx = t.x - self.x
        dy = t.y - self.y
        return math.degrees(math.atan2(-dy, dx))

    def draw(self, display):

        display.blit(self.turret_bottom, self.rect_bottom.topleft)
        if self.turret_top is not None:
            display.blit(self.turret_top, self.rect_top.topleft)

    def on_shoot(self):

        pass


class CabbageCannon(Turret):

    def __init__(self, x, y, tile_x, tile_y, bc):

        self.type = "Cabbage Cannon"

        Turret.__init__(self, x, y, tile_x, tile_y, bc,
                        turret_data["Cabbage Cannon"][0],
                        turret_data["Cabbage Cannon"][1],
                        turret_data["Cabbage Cannon"][2])

        ss = spritesheet.SpriteSheet("src/resources/turrets.png")

        self.turret_bottom = ss.get_image(0, 0, 48, 48)
        self.turret_top_image = ss.get_image(48, 0, 48, 48)
        self.turret_top = self.turret_top_image

        self.rect_bottom = self.turret_bottom.get_rect()
        self.rect_top = self.turret_top.get_rect()
        self.rect_top.topleft = self.rect_bottom.topleft = (self.x, self.y)


class JuiceRocket(Turret):

    def __init__(self, x, y, tile_x, tile_y, bc):

        self.type = "Juice Rocket"

        Turret.__init__(self, x, y, tile_x, tile_y, bc,
                        turret_data["Juice Rocket"][0],
                        turret_data["Juice Rocket"][1],
                        turret_data["Juice Rocket"][2])

        ss = spritesheet.SpriteSheet("src/resources/turrets.png")

        self.turret_bottom = ss.get_image(144, 0, 48, 48)
        self.turret_top_image = ss.get_image(96, 0, 48, 48)
        self.turret_top = self.turret_top_image

        self.rect_bottom = self.turret_bottom.get_rect()
        self.rect_top = self.turret_top.get_rect()
        self.rect_top.topleft = self.rect_bottom.topleft = (self.x, self.y)

    def on_shoot(self):

        self.board_controller.controller.sound_engine.queue_sound(("rocket_flight", 0))


class GlueGun(Turret):

    def __init__(self, x, y, tile_x, tile_y, bc):

        self.type = "Glue Gun"

        Turret.__init__(self, x, y, tile_x, tile_y, bc,
                        turret_data["Glue Gun"][0],
                        turret_data["Glue Gun"][1],
                        turret_data["Glue Gun"][2])

        ss = spritesheet.SpriteSheet("src/resources/turrets.png")

        self.turret_bottom = ss.get_image(144, 0, 48, 48)
        self.turret_top_image = ss.get_image(48, 48, 48, 48)
        self.turret_top = self.turret_top_image

        self.rect_bottom = self.turret_bottom.get_rect()
        self.rect_top = self.turret_top.get_rect()
        self.rect_top.topleft = self.rect_bottom.topleft = (self.x, self.y)
