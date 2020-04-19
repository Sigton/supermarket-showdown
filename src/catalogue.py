import pygame

from src import gui_components, spritesheet, turrets, barriers

# format: price, freq multiply, damage multiply, range multiply, money multiply
perk_data = {"Coffee": [1000, 1.25, 1, 1],
             "Pay Rise": [1750, 1, 1, 1]}


class CatalogueEntry:

    def __init__(self, x, y, icon, tooltip_text, controller, entry_type, description_image):

        self.x = x
        self.y = y

        self.controller = controller
        self.entry_type = entry_type


        self.icon = icon
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.topleft = (self.x + 15, self.y + 8)

        if entry_type == 0:
            self.price = turrets.turret_data[tooltip_text][3]
        elif entry_type == 1:
            self.price = barriers.barrier_data[tooltip_text][0]
        elif entry_type == 2:
            self.price = perk_data[tooltip_text][0]

        self.disable_time = int(1.5 * self.price)#disable_time
        self.tooltip_text = tooltip_text

        ss = spritesheet.SpriteSheet("src/resources/catalogue_backing.png")
        self.catalogue_backing_normal = ss.get_image(0, 0, 240, 48)
        self.catalogue_backing_active = ss.get_image(0, 48, 240, 48)
        self.catalogue_backing_inactive = ss.get_image(0, 96, 240, 48)

        self.catalogue_backing = self.catalogue_backing_normal

        self.refill_progress = gui_components.ProgressBar(self.x + 60, self.y + 40, 163, 4,
                                                          ((32, 32, 32), (227, 238, 192)))

        self.description = description_image

        self.rect = self.catalogue_backing.get_rect()
        self.rect.topleft = (x, y)

        text = ""
        if entry_type == 0:
            text = "Turret"
        elif entry_type == 1:
            text = "Barrier"
        elif entry_type == 2:
            text = "Perk"

        self.type_label = gui_components.Label(self.x + 60, self.y + 12, text, False, 20, (227, 238, 192))

        self.price_text = gui_components.Label(self.x, self.y + 12, "${}".format(self.price),
                                               False, 20, (227, 238, 192))
        self.price_text.rect.right = self.rect.right - 15

        self.tooltip = gui_components.Tooltip(self.tooltip_text, self.rect.right, self.rect.bottom,
                                              20, (32, 32, 32), "R")

        self.selected = False
        self.affordable = False
        self.disabled = False

        self.disabled_counter = 0

    def update(self, mouse_pos, money):

        if self.disabled_counter > 0:
            self.disabled_counter -= 1
            self.refill_progress.update(1 - self.disabled_counter/self.disable_time)
            if self.disabled_counter == 0:
                self.disabled = False

        if self.price > money or self.disabled:
            self.catalogue_backing = self.catalogue_backing_inactive
            self.tooltip.set_off()
            self.affordable = False
            return
        self.affordable = True

        if self.selected:
            self.catalogue_backing = self.catalogue_backing_active
            self.tooltip.set_on()
            self.tooltip.reposition(mouse_pos)
            return

        if self.rect.collidepoint(mouse_pos):
            self.tooltip.set_on()
            self.tooltip.reposition(mouse_pos)#(mouse_pos[0], mouse_pos[1] - self.tooltip.background.rect.height))
            self.catalogue_backing = self.catalogue_backing_active

        else:
            self.tooltip.set_off()
            self.catalogue_backing = self.catalogue_backing_normal

    def disable_for_time(self):
        self.disabled_counter = self.disable_time
        self.disabled = True

    def tooltip_check(self):
        for e in self.controller.entries:
            if e.tooltip.on and e != self:
                self.tooltip.set_off()

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def get_type(self):
        return self.entry_type

    def draw(self, display):

        display.blit(self.catalogue_backing, self.rect.topleft)
        self.price_text.draw(display)
        self.type_label.draw(display)
        display.blit(self.icon, self.icon_rect.topleft)
        if self.tooltip.on:
            display.blit(self.description, (4, 452))
        if self.disabled_counter > 0:
            self.refill_progress.draw(display)


class CatalogueManager:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        # read in icons
        ss = spritesheet.SpriteSheet("src/resources/icons.png")
        icons = [ss.get_image(0, 0, 32, 32),
                 ss.get_image(32, 0, 32, 32),
                 ss.get_image(64, 0, 32, 32),
                 ss.get_image(96, 0, 32, 32),
                 ss.get_image(0, 32, 32, 32),
                 ss.get_image(32, 32, 32, 32)]

        ss = spritesheet.SpriteSheet("src/resources/descriptions.png")
        descriptions = [ss.get_image(0, 0, 232, 264),
                        ss.get_image(232, 0, 232, 264),
                        ss.get_image(464, 0, 232, 264),
                        ss.get_image(0, 264, 232, 264),
                        ss.get_image(232, 264, 232, 264),
                        ss.get_image(464, 264, 232, 264)]

        self.entries = [CatalogueEntry(self.x, self.y, icons[1], "Barrier", self, 1, descriptions[3]),
                        CatalogueEntry(self.x, self.y + 52, icons[0], "Cabbage Cannon", self, 0, descriptions[0]),
                        CatalogueEntry(self.x, self.y + 104, icons[2], "Juice Rocket", self, 0, descriptions[1]),
                        CatalogueEntry(self.x, self.y + 156, icons[3], "Glue Gun", self, 0, descriptions[2]),
                        CatalogueEntry(self.x, self.y + 208, icons[4], "Coffee", self, 2, descriptions[4]),
                        CatalogueEntry(self.x, self.y + 260, icons[5], "Pay Rise", self, 2, descriptions[5])]

        self.entry_active = False
        self.active_entry = None

    def update(self, money):

        mouse_pos = pygame.mouse.get_pos()
        for e in self.entries:
            e.update(mouse_pos, money)

        if self.entry_active:
            self.active_entry.tooltip_check()

    def enable_all(self):

        for e in self.entries:
            e.disabled = False
            e.disabled_counter = 0

    def get_clicked(self, pos):

        for e in self.entries:
            if e.rect.collidepoint(pos):
                return e

        return None

    def set_entry_active(self, e):
        self.entry_active = True
        self.active_entry = e

        # make sure that no other entries are active
        for _e in self.entries:
            if _e.selected:
                if _e is not e:
                    _e.deselect()

    def set_entry_inactive(self):
        self.active_entry.deselect()
        self.entry_active = False
        self.active_entry = None

    def draw(self, display):

        for e in self.entries:
            e.draw(display)
        for e in self.entries:
            e.tooltip.draw(display)
