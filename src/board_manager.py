import pygame

from src import spritesheet, tile, constants
from src import customers, turrets, barriers
from src import markers, pathfinding


tile_colors = {11645361: 0,
               9079434:  1,
               5789784:  2,
               2697513:  3,
               8224198:  4,
               5658266:  5,
               5131911:  6,
               723723:   7,
               855309:   8,
               986895:   9}


def load_sprite_sheet(path):

    tile_floor = (0, 0, 48, 48)
    tarmac = (48, 0, 48, 48)
    shelf_front = (0, 48, 48, 48)
    shelf_back = (48, 48, 48, 48)
    wall_b = (0, 96, 48, 48)
    wall_r_b = (48, 96, 48, 48)
    wall_l_b = (96, 0, 48, 48)
    wall_f = (96, 48, 48, 48)
    wall_r_f = (96, 96, 48, 48)
    wall_l_f = (144, 0, 48, 48)

    tiles = [tile_floor, tarmac, shelf_front, shelf_back, wall_b, wall_r_b, wall_l_b, wall_f, wall_r_f, wall_l_f]

    sprite_sheet = spritesheet.SpriteSheet(path)

    images = []

    for t in tiles:
        images.append(sprite_sheet.get_image(t[0], t[1], t[2], t[3]))

    return images


class BoardManager:

    def __init__(self, controller):

        self.controller = controller

        self.width = 15
        self.height = 13

        self.x = 240
        self.y = 96

        self.solid_tiles = [2, 3, 4, 5, 6, 7, 8, 9]

        self.images = load_sprite_sheet("src/resources/spritesheet.png")

        self.level = []
        self.passable_tiles = [[0 for y in range(self.height+1)] for x in range(self.width)]
        self.load_terrain()

        self.customers = []
        self.turrets = []
        self.projectiles = []
        self.barriers = []

        self.update_passable_tiles()

        self.placing_spots = []
        for y in range(3, 12, 3):
            for x in range(1, 15, 2):
                self.placing_spots.append((x, y))

        self.barrier_placing_spots = []
        for y in range(self.height):
            for x in range(self.width):
                if self.passable_tiles[x][y] == 0:
                    self.barrier_placing_spots.append((x,y))

        self.turret_place_markers = [markers.Marker(s[0] * constants.TILE_RES + self.x,
                                                    s[1] * constants.TILE_RES + self.y + 12,
                                                    s[0], s[1]) for s in self.placing_spots]

        self.barrier_place_markers = [markers.Marker(s[0] * constants.TILE_RES + self.x,
                                                    s[1] * constants.TILE_RES + self.y + 12,
                                                    s[0], s[1]) for s in self.barrier_placing_spots]

        self.update_barrier_place_markers()

        # AI OPTIMISATIONS
        self.ai_paths = []
        for spawn in constants.SPAWN_POINTS:
            self.ai_paths.append(pathfinding.search(self.passable_tiles, 5, spawn, constants.PATHFINDING_GOAL))

        self.place_backing = pygame.Surface([self.width * constants.TILE_RES, self.height * constants.TILE_RES])
        self.place_backing.set_alpha(127)
        self.place_backing.fill((127,127,127))

        self.place_mode = False
        self.placing_turrets = False
        self.placing_barriers = False

        self.turret_ring = None
        self.turret_ring_rect = None
        self.show_turret_ring = False

        self.turret_type = ""

        self.freq_mul = 1
        self.damage_mul = 1
        self.range_mul = 1

    def load_terrain(self):

        map_image = pygame.image.load("src/resources/map.png")
        self.level = []
        pixel_array = pygame.PixelArray(map_image)

        x = 0
        for column in pixel_array:
            y = 0
            for pixel in column:
                if pixel in tile_colors:
                    self.level.append(tile.Tile(x * constants.TILE_RES + self.x, y * constants.TILE_RES + self.y,
                                                self.images[tile_colors[pixel]]))
                    if tile_colors[pixel] in self.solid_tiles:
                        self.passable_tiles[x][y] = 1
                y += 1
            x += 1

    def update_passable_tiles(self):
        for b in self.barriers:
            self.passable_tiles[b.tile_x][b.tile_y] = 1

        self.ai_paths = []
        for spawn in constants.SPAWN_POINTS:
            self.ai_paths.append(pathfinding.search(self.passable_tiles, 5, spawn, constants.PATHFINDING_GOAL))

        for c in self.customers:
            c.recalculate_path()

    def update_barrier_place_markers(self):
        to_delete = []
        for s in self.barrier_placing_spots:

            if self.passable_tiles[s[0]][s[1]] == 1:
                # this spot already has something on it
                to_delete += [s]
                continue

            # a superb optimisation:
            # if s is not in the current optimal path from any spawn point,
            # then blocking it will not remove all possible paths from spawn to goal
            s_is_used = False
            for path in self.ai_paths:
                if s in path:
                    s_is_used = True
            if not s_is_used:
                continue

            temp_map = self.passable_tiles
            temp_map[s[0]][s[1]] = 1

            for spawn in constants.SPAWN_POINTS:
                if pathfinding.search(temp_map, 1, spawn, constants.PATHFINDING_GOAL) in (False, None):
                    # if the barrier is placed here, then there is no possible goal from start to finish
                    if s not in to_delete:
                        to_delete += [s]
                        break

            temp_map[s[0]][s[1]] = 0

        for s in to_delete:
            self.barrier_placing_spots.remove(s)
            self.barrier_place_markers.remove(self.get_barrier_marker_at_pos(s[0], s[1]))

    def create_turret_ring(self, radius, x, y):

        self.show_turret_ring = True
        self.turret_ring = pygame.Surface([radius * 2, radius * 2])
        self.turret_ring.set_colorkey((0, 0, 0))
        self.turret_ring_rect = pygame.draw.circle(self.turret_ring, (255, 0, 0), (radius, radius), radius, 1)
        self.turret_ring_rect.center = (x,y)

    def place_turret(self, t, tx, ty):

        t0 = self.get_turret_at_pos(tx, ty)
        if t0 is not None:
            self.turrets.remove(t0)

        if t == "Cabbage Cannon":
            self.turrets.append(turrets.CabbageCannon(tx * constants.TILE_RES + self.x,
                                                      ty * constants.TILE_RES + self.y,
                                                      tx, ty, self))
        elif t == "Juice Rocket":
            self.turrets.append(turrets.JuiceRocket(tx * constants.TILE_RES + self.x,
                                                    ty * constants.TILE_RES + self.y,
                                                    tx, ty, self))

        elif t == "Glue Gun":
            self.turrets.append(turrets.GlueGun(tx * constants.TILE_RES + self.x,
                                                ty * constants.TILE_RES + self.y,
                                                tx, ty, self))

    def place_barrier(self, b, bx, by):

        if b == "Barrier":
            self.barriers.append(barriers.Barrier(bx * constants.TILE_RES + self.x,
                                                  by * constants.TILE_RES + self.y,
                                                  bx, by))

        self.update_passable_tiles()
        self.update_barrier_place_markers()

    def spawn_customer(self, x, y, customer_type):

        self.customers.append(customer_type(x * constants.TILE_RES + self.x,
                                            y * constants.TILE_RES + self.y,
                                            x, y, self))

    def apply_perk(self, t):

        if t == "Coffee":
            self.freq_mul = 2

    def reset_perks(self):

        self.freq_mul = 1
        self.damage_mul = 1
        self.range_mul = 1

    def update(self):

        for c in self.customers:
            c.update()

        for t in self.turrets:
            t.update()

        for p in self.projectiles:
            p.update()

        if self.place_mode:
            if self.placing_turrets:

                mouse_pos = pygame.mouse.get_pos()
                touching_any = False
                for m in self.turret_place_markers:
                    if m.active:
                        if m.rect.collidepoint(mouse_pos):
                            touching_any = True
                            # mouse is over the marker: we want to draw the range of the turret
                            self.create_turret_ring(turrets.turret_data[self.turret_type][1],
                                                    m.rect.centerx, m.rect.centery)
                if not touching_any:
                    self.show_turret_ring = False

    def get_num_customers(self):

        return len(self.customers)

    def set_active_turret_type(self, turret_type):
        self.turret_type = turret_type

    def touching_place_marker(self, mouse_pos):

        for m in self.turret_place_markers:
            if m.rect.collidepoint(mouse_pos):
                return m
        return None

    def touching_barrier_place_marker(self, mouse_pos):

        for m in self.barrier_place_markers:
            if m.rect.collidepoint(mouse_pos):
                return m
        return None

    def draw(self, display):

        for t in self.level:
            t.draw(display)

        for c in sorted(self.customers, key=lambda x: x.rect.bottom):
            c.draw(display)

        for b in self.barriers:
            b.draw(display)

        for t in self.turrets:
            t.draw(display)

        for p in self.projectiles:
            p.draw(display)

        if self.place_mode:
            display.blit(self.place_backing, (self.x, self.y))

            if self.placing_turrets:
                for m in self.turret_place_markers:
                    if m.active: m.draw(display)
                if self.show_turret_ring:
                    display.blit(self.turret_ring, self.turret_ring_rect.topleft)

            else:
                for m in self.barrier_place_markers:
                    m.draw(display)

    def get_turret_at_pos(self, x, y):

        for t in self.turrets:
            if t.tile_x == x and t.tile_y == y:
                return t
        return None

    def get_turret_marker_at_pos(self, x, y):

        for t in self.turret_place_markers:
            if t.tile_x == x and t.tile_y == y:
                return t
        return None

    def get_barrier_marker_at_pos(self, x, y):

        for t in self.barrier_place_markers:
            if t.tile_x == x and t.tile_y == y:
                return t
        return None

    def set_placing(self, t=False, b=False):

        self.place_mode = True
        self.placing_barriers = b
        self.placing_turrets = t

    def disable_placing(self):

        self.place_mode = False
        self.placing_turrets = False
        self.placing_barriers = False

    def setup_turret_markers(self, turret_type):

        for m in self.turret_place_markers:
            t = self.get_turret_at_pos(m.tile_x, m.tile_y)
            if t is None:
                m.set_active()
            else:
                if t.type == turret_type:
                    m.set_inactive()
                else:
                    m.set_active()

    def reset(self):

        self.level = []
        self.passable_tiles = [[0 for y in range(self.height + 1)] for x in range(self.width)]
        self.load_terrain()

        self.customers = []
        self.turrets = []
        self.projectiles = []
        self.barriers = []

        self.update_passable_tiles()

        self.barrier_placing_spots = []
        for y in range(self.height):
            for x in range(self.width):
                if self.passable_tiles[x][y] == 0:
                    self.barrier_placing_spots.append((x, y))

        self.turret_place_markers = [markers.Marker(s[0] * constants.TILE_RES + self.x,
                                                    s[1] * constants.TILE_RES + self.y + 12,
                                                    s[0], s[1]) for s in self.placing_spots]

        self.barrier_place_markers = [markers.Marker(s[0] * constants.TILE_RES + self.x,
                                                     s[1] * constants.TILE_RES + self.y + 12,
                                                     s[0], s[1]) for s in self.barrier_placing_spots]

        self.update_barrier_place_markers()

        # AI OPTIMISATIONS
        self.ai_paths = []
        for spawn in constants.SPAWN_POINTS:
            self.ai_paths.append(pathfinding.search(self.passable_tiles, 5, spawn, constants.PATHFINDING_GOAL))

        self.place_mode = False
        self.placing_turrets = False
        self.placing_barriers = False

        self.turret_ring = None
        self.turret_ring_rect = None
        self.show_turret_ring = False

        self.turret_type = ""

        self.freq_mul = 1
        self.damage_mul = 1
        self.range_mul = 1
