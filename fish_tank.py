import random
import shutil
import sys
import time


class Settings:
    """A class to store all settings for fish_tank."""

    def __init__(self):
        self.framerate = 5
        self.fish_count = 100

        self.size = shutil.get_terminal_size()
        self.width = self.size.columns
        self.height = self.size.lines

        self.reset_code = "\033[0m"
        self.color_codes = {
            "red": "\033[31m",
            "orange": "\033[38;5;208m",
            "yellow": "\033[33m",
            "green": "\033[32m",
            "blue": "\033[34m",
            "indigo": "\033[38;5;63m",
            "violet": "\033[38;5;93m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
        }


class Fish:
    """A class to store all information about a fish."""

    def __init__(self):
        self.settings = Settings()
        self.sprites = {1: "><>", -1: "<><"}
        self.position = [
            random.randint(0, self.settings.height - 2),
            random.randint(0, self.settings.width - 3),
        ]
        self.direction = random.choice((1, -1))
        self.color = random.choice(list(self.settings.color_codes.keys()))

    def swim(self):
        if random.random() < 0.02:
            self.change_direction()

        if self.would_hit_edge():
            self.change_direction()

        self.position[1] += self.direction

    def would_hit_edge(self):
        next_x = self.position[1] + self.direction
        return next_x > self.settings.width - 3 or next_x < 0

    def change_direction(self):
        self.direction *= -1


class FishTank:
    """Overall class to manage fish_tank assets and behavior."""

    def __init__(self):
        """Initialize fish_tank and create animation resources"""
        self.settings = Settings()
        self.school = self.create_school()

    def play_animation(self):
        while True:
            self.reset_grid()
            self.prep_grid()
            self.print_grid()
            self.update_fish()
            time.sleep(1 / self.settings.framerate)

    def reset_grid(self):
        self.grid = [
            [" " for _ in range(self.settings.width)]
            for _ in range(self.settings.height)
        ]

    def prep_grid(self):
        reset = self.settings.reset_code

        # Insert fish
        for fish in self.school:
            sprite = fish.sprites[fish.direction]
            color = self.settings.color_codes[fish.color]

            for i, char in enumerate(sprite):
                self.grid[fish.position[0]][fish.position[1] + i] = color + char + reset

        # Insert sand
        yellow = self.settings.color_codes["yellow"]
        for i in range(self.settings.width):
            self.grid[self.settings.height - 1][i] = yellow + "░" + reset

    def print_grid(self):
        print("\033[H", end="")
        for row in self.grid:
            print("".join(row), end="")
        sys.stdout.flush()

    def update_fish(self):
        for fish in self.school:
            fish.swim()

    def create_school(self):
        return [Fish() for _ in range(self.settings.fish_count)]


if __name__ == "__main__":
    fish_tank = FishTank()
    try:
        fish_tank.play_animation()
    except KeyboardInterrupt:
        sys.exit()
