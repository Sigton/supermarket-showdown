import pygame


class SoundEngine:

    def __init__(self):

        pygame.mixer.set_num_channels(16)

        self.button_click_channel = pygame.mixer.Channel(0)
        self.turret_place_channel = pygame.mixer.Channel(1)
        self.life_lost_channel = pygame.mixer.Channel(2)
        self.daily_bonus_channel = pygame.mixer.Channel(3)
        self.projectile_fire_channel = pygame.mixer.Channel(4)
        self.perk_used_channel = pygame.mixer.Channel(5)
        self.rocket_impact_channel = pygame.mixer.Channel(6)
        self.salary_gain_channel = pygame.mixer.Channel(7)
        self.footstep_channel = pygame.mixer.Channel(8)
        self.glue_impact_channel = pygame.mixer.Channel(9)
        self.hit_channel = pygame.mixer.Channel(10)
        self.game_over_channel = pygame.mixer.Channel(11)
        self.game_start_channel = pygame.mixer.Channel(12)
        self.music_channel = pygame.mixer.Channel(13)
        self.rocket_flight_channel = pygame.mixer.Channel(14)
        self.typewriter_channel = pygame.mixer.Channel(15)

        self.button_click = pygame.mixer.Sound("src/resources/button_click.wav")
        self.turret_place = pygame.mixer.Sound("src/resources/turret_place.wav")
        self.life_lost = pygame.mixer.Sound("src/resources/life_lost.wav")
        self.daily_bonus = pygame.mixer.Sound("src/resources/daily_bonus.wav")
        self.projectile_fire = pygame.mixer.Sound("src/resources/projectile_fire.wav")
        self.perk_used = pygame.mixer.Sound("src/resources/perk_used.wav")
        self.rocket_impact = pygame.mixer.Sound("src/resources/rocket_impact.wav")
        self.salary_gain = pygame.mixer.Sound("src/resources/salary_gain.wav")
        self.footstep = pygame.mixer.Sound("src/resources/footstep.wav")
        self.glue_impact = pygame.mixer.Sound("src/resources/glue_impact.wav")
        self.hit = pygame.mixer.Sound("src/resources/hit.wav")
        self.game_over = pygame.mixer.Sound("src/resources/game_over.wav")
        self.game_start = pygame.mixer.Sound("src/resources/game_start.wav")
        self.music = pygame.mixer.Sound("src/resources/music.wav")
        self.rocket_flight = pygame.mixer.Sound("src/resources/rocket_flight.wav")
        self.typewriter = pygame.mixer.Sound("src/resources/typewriter.wav")

        self.channel_linkup = {
            "button_click": self.button_click_channel,
            "turret_place": self.turret_place_channel,
            "life_lost": self.life_lost_channel,
            "daily_bonus": self.daily_bonus_channel,
            "projectile_fire": self.projectile_fire_channel,
            "perk_used": self.perk_used_channel,
            "rocket_impact": self.rocket_impact_channel,
            "salary_gain": self.salary_gain_channel,
            "footstep": self.footstep_channel,
            "glue_impact": self.glue_impact_channel,
            "hit": self.hit_channel,
            "game_over": self.game_over_channel,
            "game_start": self.game_start_channel,
            "music": self.music_channel,
            "rocket_flight": self.rocket_flight_channel,
            "typewriter": self.typewriter_channel
        }

        self.sound_linkup = {
            "button_click": self.button_click,
            "turret_place": self.turret_place,
            "life_lost": self.life_lost,
            "daily_bonus": self.daily_bonus,
            "projectile_fire": self.projectile_fire,
            "perk_used": self.perk_used,
            "rocket_impact": self.rocket_impact,
            "salary_gain": self.salary_gain,
            "footstep": self.footstep,
            "glue_impact": self.glue_impact,
            "hit": self.hit,
            "game_over": self.game_over,
            "game_start": self.game_start,
            "music": self.music,
            "rocket_flight": self.rocket_flight,
            "typewriter": self.typewriter
        }

        self.queued_sounds = []

        self.music.set_volume(0.5)
        self.footstep.set_volume(0.5)
        self.rocket_flight.set_volume(0.5)
        self.typewriter.set_volume(0.3)
        self.salary_gain.set_volume(0.8)

    def play_sounds(self):
        [self.channel_linkup[sound[0]].play(self.sound_linkup[sound[0]], sound[1]) for sound in self.queued_sounds]
        self.queued_sounds = []

    def queue_sound(self, sound):
        self.queued_sounds.append(sound)

    def stop_sound(self, sound):
        self.channel_linkup[sound].stop()