from src import spritesheet, constants
from src import pathfinding
from src import gui_components


class Customer:

    def __init__(self, x, y, tile_x, tile_y, bc):

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = x
        self.y = y

        self.board_controller = bc

        self.run_r_frames = []
        self.run_l_frames = []
        self.stand_r = []
        self.stand_l = []

        self.image = None
        self.rect = None

        self.health_bar = gui_components.ProgressBar(x, y - 10, 36, 6, ((32, 32, 32), (174, 186, 137)))
        self.health_bar.update(1)

        self.max_hp = 100
        self.hp = 100

        self.path = []
        self.recalculate_path()

        self.movement = (0, 0)
        self.move_steps = 0
        self.speed = constants.CUSTOMER_MOVE_SPEED

        self.wait_timer = 0

        self.anim_image = 0
        self.anim_timer = 0

    def recalculate_path(self):
        # try and see if we can use one of the existing paths calculated in the board controller
        self.path = []
        for path in self.board_controller.ai_paths:
            if (self.tile_x, self.tile_y) in path:
                self.path = path[path.index((self.tile_x, self.tile_y)):]
                return

        # didnt find a path in the cache
        self.path = pathfinding.search(self.board_controller.passable_tiles, 5,
                                      (self.tile_x, self.tile_y), constants.PATHFINDING_GOAL)

    def update(self):

        if self.wait_timer > 0:
            self.wait_timer -= 1
            self.image = self.stand_r if self.movement[0] > 0 else self.stand_l
            return

        if self.move_steps == 0:

            if len(self.path) == 0:
                # we have reached the door!
                self.board_controller.controller.lives -= 1
                self.board_controller.customers.remove(self)
                self.board_controller.controller.sound_engine.queue_sound(("life_lost", 0))

                self.hp = 0
                return

            if self.path[0] == (self.tile_x, self.tile_y):
                self.path = self.path[1:]

            self.move_steps = constants.TILE_RES / self.speed
            self.movement = ((self.path[0][0] - self.tile_x) * self.speed,
                             (self.path[0][1] - self.tile_y) * self.speed)
            self.tile_x = self.path[0][0]
            self.tile_y = self.path[0][1]

            self.path = self.path[1:]
        else:
            self.move_steps -= 1
            self.x += self.movement[0]
            self.y += self.movement[1]

            self.anim_timer += 1
            if self.anim_timer == constants.CUSTOMER_ANIM_SPEED:

                self.anim_timer = 0
                self.anim_image = (self.anim_image + 1) % 4
                if self.movement[0] > 0:
                    self.image = self.run_r_frames[self.anim_image]
                else:
                    self.image = self.run_l_frames[self.anim_image]

        self.rect.topleft = (self.x, self.y)
        self.health_bar.rect.center = (self.rect.centerx, self.rect.y - 10)

    def delay(self, amount):

        self.wait_timer = amount

    def damage(self, amount):

        self.hp -= amount
        self.health_bar.update(self.hp/self.max_hp)

        if self.hp <= 0:
            self.board_controller.customers.remove(self)

    def draw(self, display):

        display.blit(self.image, self.rect.topleft)
        self.health_bar.draw(display)


class RegularCustomer(Customer):

    def __init__(self, x, y, tile_x, tile_y, bc):

        Customer.__init__(self, x, y, tile_x, tile_y, bc)

        ss = spritesheet.SpriteSheet("src/resources/customers.png")

        self.run_r_frames = [ss.get_image(0, 0, 48, 48),
                             ss.get_image(48, 0, 48, 48),
                             ss.get_image(96, 0, 48, 48),
                             ss.get_image(144, 0, 48, 48)]
        self.run_l_frames = [ss.get_image(0, 48, 48, 48),
                             ss.get_image(48, 48, 48, 48),
                             ss.get_image(96, 48, 48, 48),
                             ss.get_image(144, 48, 48, 48)]

        self.stand_r = self.run_r_frames[0]
        self.stand_l = self.run_l_frames[0]

        self.image = self.stand_r
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class FastCustomer(Customer):

    def __init__(self, x, y, tile_x, tile_y, bc):

        Customer.__init__(self, x, y, tile_x, tile_y, bc)

        ss = spritesheet.SpriteSheet("src/resources/customers.png")

        self.run_r_frames = [ss.get_image(0, 96, 48, 48),
                             ss.get_image(48, 96, 48, 48),
                             ss.get_image(96, 96, 48, 48),
                             ss.get_image(144, 96, 48, 48)]
        self.run_l_frames = [ss.get_image(0, 144, 48, 48),
                             ss.get_image(48, 144, 48, 48),
                             ss.get_image(96, 144, 48, 48),
                             ss.get_image(144, 144, 48, 48)]

        self.stand_r = self.run_r_frames[0]
        self.stand_l = self.run_l_frames[0]

        self.image = self.stand_r
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed *= 2

customer_options = [RegularCustomer, FastCustomer]
