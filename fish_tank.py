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


class Fish:
    """A class to store all information about a fish."""

    def __init__(self):
        self.ascii = {"right": "><>", "left": "<><"}
        self.position = [5, 20]
        self.speed = random.randint(1, 2)

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
        self.grid[self.fish.position[0]][self.fish.position[1]] = self.fish.ascii[
            "right"
        ]

    def print_grid(self):
        for row in self.grid:
            print("".join(row))


if __name__ == "__main__":
    fish_tank = FishTank()
    fish_tank.play_animation()
