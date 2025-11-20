import random
import shutil
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
        self.ascii = {"right": "><>", "left": "<><"}
        self.position = [5, 20]
        self.speed = random.randint(1, 2)
        self.color = random.choice(list(self.settings.color_codes.keys()))

    def swim(self):
        self.position[1] += self.speed


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
        for i, char in enumerate(self.fish.ascii["right"]):
            self.grid[self.fish.position[0]][self.fish.position[1] + i] = (
                self.settings.color_codes[self.fish.color]
                + char
                + self.settings.reset_code
            )

    def print_grid(self):
        for row in self.grid:
            print("".join(row))


if __name__ == "__main__":
    fish_tank = FishTank()
    fish_tank.play_animation()
