from src import customers, constants

import random


class WaveGenerator:

    def __init__(self):
        self.variance = constants.VARIANCE
        self.variance_mul = 1

        self.spawn_points = [(4, -1), (10, -1)]

        self.customer_selector = [0]

    def generate_wave(self, num, wave_num):
        wave = []
        n = random.randint(max(2, int((num - self.variance) * self.variance_mul)),
                           int((num + self.variance) * self.variance_mul))

        delays = [random.randint(5,100) for n in range(n)]
        delays = sorted([int(d * 11 * constants.DAY_LENGTH / sum(delays)) for d in delays])

        for n in range(n):
            wave.append((customers.customer_options[random.choice(self.customer_selector)],
                         delays[n],
                         random.choice(self.spawn_points)))
        self.variance_mul += 0.2

        if wave_num >= 3:
            self.customer_selector += [0, 1]

        return wave
