import pygame

from src import spritesheet

import math

# format: speed, delay, damage
projectile_data = {
    "Cabbage": [5, 0, 20],
    "Rocket": [3, 0, 40],
    "Glue": [7, 50, 5]
}


class Projectile:

    def __init__(self, x, y, target, move_speed, delay_amount, damage):

        self.x = x
        self.y = y
        self.target = target

        # movement in each direction that projectile needs to move
        self.dx = 0
        self.dy = 0

        self.move_speed = move_speed
        self.delay_amount = delay_amount
        self.damage = damage

        self.image_original = None
        self.image = None
        self.rect = None

        self.clear = False
        self.clear_timer = 5

    def face_target(self):
        self.dx = self.target.rect.centerx - self.rect.centerx
        self.dy = self.target.rect.centery - self.rect.centery

        a = math.degrees(math.atan2(-self.dy, self.dx)) - 90
        self.image = pygame.transform.rotate(self.image_original, a)
        self.rect = self.image.get_rect(center=self.rect.center)

    def normalize_move_vector(self):

        d = math.hypot(self.dx, self.dy)
        if d == 0:
            return
        self.dx /= d
        self.dy /= d
        self.dx *= self.move_speed
        self.dy *= self.move_speed

    def update(self):

        self.face_target()
        self.normalize_move_vector()

        self.x += self.dx
        self.y += self.dy

        self.rect.topleft = (self.x, self.y)

        if self.rect.colliderect(self.target.rect):
            self.clear = True

        if self.target.hp <= 0:
            # target has died, we can find a new target
            new_target = self.find_closest_target()
            if new_target is not None:
                self.target = new_target

        if self.clear:
            if self.clear_timer == 0:
                self.target.board_controller.projectiles.remove(self)
                if self.target.hp > 0:
                    self.target.delay(self.delay_amount)
                    self.target.damage(self.damage)
                    self.on_impact()
            else: self.clear_timer -= 1

    def find_closest_target(self):
        new_target = None
        closest = math.inf
        for c in self.target.board_controller.customers:
            dx = c.x - self.x
            dy = c.y - self.y
            d = (dx * dx) + (dy * dy)
            if d < closest:
                closest = d
                new_target = c
        return new_target

    def on_impact(self):

        pass

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)


class Cabbage(Projectile):

    def __init__(self, x, y, target):

        Projectile.__init__(self, x, y, target,
                            projectile_data["Cabbage"][0],
                            projectile_data["Cabbage"][1],
                            projectile_data["Cabbage"][2])

        ss = spritesheet.SpriteSheet("src/resources/cabbage.png")
        self.image = ss.get_image(0, 0, 18, 16)
        self.image_original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x, self.y = self.rect.topleft

        self.face_target()
        self.normalize_move_vector()

    def on_impact(self):

        self.target.board_controller.controller.sound_engine.queue_sound(("hit", 0))

class Rocket(Projectile):

    def __init__(self, x, y, target):

        Projectile.__init__(self, x, y, target,
                            projectile_data["Rocket"][0],
                            projectile_data["Rocket"][1],
                            projectile_data["Rocket"][2])

        ss = spritesheet.SpriteSheet("src/resources/rocket.png")
        self.image = ss.get_image(0, 0, 18, 25)
        self.image_original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x, self.y = self.rect.topleft

        self.face_target()
        self.normalize_move_vector()

    def on_impact(self):

        self.target.board_controller.controller.sound_engine.queue_sound(("rocket_impact", 0))


class Glue(Projectile):

    def __init__(self, x, y, target):

        Projectile.__init__(self, x, y, target,
                            projectile_data["Glue"][0],
                            projectile_data["Glue"][1],
                            projectile_data["Glue"][2])

        ss = spritesheet.SpriteSheet("src/resources/glue.png")
        self.image = ss.get_image(0, 0, 9, 21)
        self.image_original = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x, self.y = self.rect.topleft

        self.face_target()
        self.normalize_move_vector()

    def on_impact(self):

        self.target.board_controller.controller.sound_engine.queue_sound(("glue_impact", 0))
