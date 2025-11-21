import random
import shutil
import sys
import time


class Settings:
    """A class to store all settings for fish_tank."""

    def __init__(self):
        self.framerate = 4

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
            random.randint(0, self.settings.height - 3),
            random.randint(0, self.settings.width - 1),
        ]
        self.direction = random.choice((1, -1))
        self.speed = random.choice((1, 2))
        self.color = random.choice(list(self.settings.color_codes.keys()))

    def swim(self):
        self.position[1] += self.speed * self.direction


class FishTank:
    """Overall class to manage fish_tank assets and behavior."""

    def __init__(self):
        """Initialize fish_tank and create animation resources"""
        self.settings = Settings()
        self.fish = Fish()

    def play_animation(self):
        while True:
            self.reset_grid()
            self.prep_grid()
            self.print_grid()
            self.fish.swim()
            time.sleep(1 / self.settings.framerate)

    def reset_grid(self):
        self.grid = [
            [" " for _ in range(self.settings.width)]
            for _ in range(self.settings.height)
        ]

    def prep_grid(self):
        # Insert fish
        for i, char in enumerate(self.fish.sprites[self.fish.direction]):
            self.grid[self.fish.position[0]][self.fish.position[1] + i] = (
                self.settings.color_codes[self.fish.color]
                + char
                + self.settings.reset_code
            )
        # Insert sand
        for i in range(self.settings.width):
            self.grid[self.settings.height - 1][i] = (
                self.settings.color_codes["yellow"] + "░" + self.settings.reset_code
            )

    def print_grid(self):
        print("\033[H", end="")
        for row in self.grid:
            print("".join(row), end="")
        sys.stdout.flush()


if __name__ == "__main__":
    fish_tank = FishTank()
    try:
        fish_tank.play_animation()
    except KeyboardInterrupt:
        sys.exit()
