import pygame
from pygame.locals import *

from src import constants
from src import board_manager, hud, slideshow
from src import barriers, turrets
from src import wave_gen, sounds

class Main:

    def __init__(self):

        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.display = pygame.display.set_mode(constants.RESOLUTION)
        pygame.display.set_caption("Supermarket Showdown")

        icon = pygame.image.load("src/resources/icon.png").convert_alpha()
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()

        self.board_manager = board_manager.BoardManager(self)
        self.hud = hud.HUD()

        self.sound_engine = sounds.SoundEngine()

        self.wave_generator = wave_gen.WaveGenerator()
        self.wave_size = constants.INIT_WAVE_SIZE
        self.wave_size_mul = constants.WAVE_SIZE_MUL
        self.current_wave = self.wave_generator.generate_wave(self.wave_size, 1)

        self.salary = constants.INITIAL_SALARY
        self.additional_salary = 0
        self.money = constants.INITIAL_MONEY
        self.day = 1
        self.hour = 0

        self.lives = 3

        self.timer = constants.DAY_LENGTH
        self.spawn_timer = 0

        self.daily_bonus_timer = 0

        self.go_hud = False

        self.intro = slideshow.Slideshow(self)

    def run(self):

        self.sound_engine.queue_sound(("typewriter", -1))
        self.sound_engine.play_sounds()
        game_exit = self.intro.run()
        self.sound_engine.stop_sound("typewriter")

        self.sound_engine.queue_sound(("music", -1))
        self.sound_engine.queue_sound(("game_start", 0))

        while not game_exit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_exit = True

                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.lives <= 0:

                            self.sound_engine.queue_sound(("button_click", 0))

                            self.reset()
                            self.board_manager.reset()
                            self.hud.game_over.begin_move_out()

                            self.sound_engine.queue_sound(("game_start", 0))

                        else:
                            # check if we have clicked on something in the catalogue
                            e = self.hud.cat_man.get_clicked(pygame.mouse.get_pos())
                            if e is not None and e.affordable:
                                self.sound_engine.queue_sound(("button_click", 0))
                                # if this turret is already selected we need to deselect it
                                if e.selected:

                                    e.deselect()
                                    self.hud.cat_man.set_entry_inactive()

                                    self.board_manager.disable_placing()

                                else:
                                    if e.get_type() == 2:
                                        # we have clicked on a perk; perk must now be applied
                                        if e.tooltip_text != "Pay Rise":
                                            self.board_manager.apply_perk(e.tooltip_text)
                                        else:
                                            self.additional_salary = int(self.salary / 2)
                                        e.disabled = True
                                        self.sound_engine.queue_sound(("perk_used", 0))

                                        self.money -= hud.catalogue.perk_data[e.tooltip_text][0]
                                    else:
                                        self.hud.cat_man.set_entry_active(e)
                                        e.select()
                                        # now that an item has been selected, we need to allow it to be placed
                                        c = e.get_type() == 0
                                        self.board_manager.set_placing(c, not c)
                                        self.board_manager.set_active_turret_type(e.tooltip_text)
                                        self.board_manager.setup_turret_markers(e.tooltip_text)
                            elif self.board_manager.place_mode:

                                # check if were placing turrets or barriers:
                                if self.board_manager.placing_turrets:
                                    # check if we clicked on a placing spot
                                    t = self.board_manager.touching_place_marker(pygame.mouse.get_pos())
                                    if t is not None:
                                        # then we can finally place a turret, and disable all the selection stuff
                                        turret_name = self.hud.cat_man.active_entry.tooltip_text
                                        self.hud.cat_man.active_entry.disable_for_time()

                                        self.board_manager.place_turret(turret_name, t.tile_x, t.tile_y)
                                        self.hud.cat_man.set_entry_inactive()
                                        self.board_manager.disable_placing()

                                        # deduct balance
                                        self.money -= turrets.turret_data[turret_name][3]

                                        self.sound_engine.queue_sound(("turret_place", 0))

                                else:
                                    # check if we clicked on a placing spot
                                    b = self.board_manager.touching_barrier_place_marker(pygame.mouse.get_pos())
                                    if b is not None:
                                        # then place a barrier
                                        barrier_name = self.hud.cat_man.active_entry.tooltip_text
                                        self.hud.cat_man.active_entry.disable_for_time()

                                        self.board_manager.place_barrier(barrier_name, b.tile_x, b.tile_y)
                                        self.hud.cat_man.set_entry_inactive()
                                        self.board_manager.disable_placing()

                                        # deduct balance
                                        self.money -= barriers.barrier_data[barrier_name][0]

                                        self.sound_engine.queue_sound(("turret_place", 0))

            # UPDATE STUFF HERE

            if len(self.current_wave) > 0:
                self.spawn_timer += 1
                if self.spawn_timer == self.current_wave[0][1]:
                    # time to spawn a customer
                    c = self.current_wave[0]
                    p = c[2]
                    self.board_manager.spawn_customer(p[0], p[1], c[0])
                    self.spawn_timer = 0
                    self.current_wave = self.current_wave[1:]

            if self.lives > 0:
                if self.timer > 0:
                    self.timer -= 1
                    if self.timer % 40 == 0 and self.board_manager.get_num_customers() > 0:
                        self.sound_engine.queue_sound(("footstep", 0))
                else:
                    if self.hour < 12:
                        self.timer = constants.DAY_LENGTH
                        self.hour += 1
                        self.money += (self.salary + self.additional_salary)
                        self.sound_engine.queue_sound(("salary_gain", 0))

                    else:
                        if not self.board_manager.get_num_customers():
                            self.hour = 0
                            self.day += 1

                            self.wave_size = int(self.wave_size * self.wave_size_mul)
                            self.current_wave = self.wave_generator.generate_wave(self.wave_size, self.day)

                            self.hud.daily_bonus.begin_move_in()
                            self.daily_bonus_timer = 150
                            self.money += 500
                            self.salary += 25

                            self.sound_engine.queue_sound(("daily_bonus", 0))

                            self.board_manager.reset_perks()
                            self.additional_salary = 0
                            self.hud.cat_man.enable_all()

                if self.daily_bonus_timer > 0:
                    self.daily_bonus_timer -= 1
                    if self.daily_bonus_timer == 0:
                        self.hud.daily_bonus.begin_move_out()

                self.board_manager.update()
            else:
                if not self.go_hud:
                    self.sound_engine.queue_sound(("game_over", 0))
                    self.hud.game_over.begin_move_in()
                    self.go_hud = True

            self.hud.update(self.money, self.salary + self.additional_salary, self.day, self.hour, self.lives)

            self.sound_engine.play_sounds()

            self.display.fill(constants.BLACK)

            # DRAW TO DISPLAY HERE

            self.board_manager.draw(self.display)
            self.hud.draw(self.display)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def reset(self):

        self.wave_size = constants.INIT_WAVE_SIZE
        self.wave_size_mul = constants.WAVE_SIZE_MUL
        self.current_wave = self.wave_generator.generate_wave(self.wave_size, 1)

        self.salary = constants.INITIAL_SALARY
        self.money = constants.INITIAL_MONEY
        self.day = 1
        self.hour = 0

        self.lives = 3

        self.timer = constants.DAY_LENGTH
        self.spawn_timer = 0

        self.daily_bonus_timer = 0

        self.go_hud = False


if __name__ == "__main__":
    app = Main()
    app.run()
    quit()
