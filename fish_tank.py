import random
import shutil
import sys
import time


class Settings:
    """A class to store all settings for fish_tank."""

    def __init__(self):
        self.framerate = 5
        self.fish_count = 12
        self.kelp_count = 7
        self.bubbler_count = 2

        self.size = shutil.get_terminal_size()
        self.width = self.size.columns
        self.height = self.size.lines


class Colors:
    """A class to store color codes."""

    def __init__(self):
        self.reset = "\033[0m"

        self.colors = [
            "\033[31m",  # Red
            "\033[38;5;208m",  # Orange
            "\033[33m",  # Yellow
            "\033[32m",  # Green
            "\033[34m",  # Blue
            "\033[38;5;63m",  # Indigo
            "\033[38;5;93m",  # Violet
            "\033[35m",  # Magenta
            "\033[36m",  # Cyan
        ]


class Sprites:
    """A class to store sprites."""

    def __init__(self):
        self.fish_sprites = [
            {1: "><>", -1: "<><"},
            {1: ">||>", -1: "<||<"},
            {1: ">))>", -1: "<((<"},
            {1: ">-==>", -1: "<==-<"},
            {1: r">\\>", -1: "<//<"},
            {1: "><)))*>", -1: "<*(((><"},
            {1: "}-[[[*>", -1: "<*]]]-{"},
            {1: "><XXX*>", -1: "<*XXX><"},
        ]


class Fish:
    """A class to store all information about a fish."""

    def __init__(self):
        self.settings = Settings()
        self.sprite = random.choice(Sprites().fish_sprites)
        self.color = random.choice(Colors().colors)
        self.direction = random.choice((1, -1))
        self.position = [
            random.randint(0, self.settings.height - 2),
            random.randint(0, self.settings.width - len(self.sprite[self.direction])),
        ]
        self.direction_cooldown = 0

    def swim(self):
        if self.would_hit_horizontal_edge():
            self.change_direction()
            self.direction_cooldown = 5
            return

        r = random.random()

        if r < 0.03:
            self.change_altitude()
        elif r < 0.06 and self.direction_cooldown == 0:
            self.change_direction()
            self.direction_cooldown = 5
        elif r < 0.56:
            self.position[1] += self.direction

        self.direction_cooldown = max(0, self.direction_cooldown - 1)

    def change_altitude(self):
        y = self.position[0]
        min_y = 0
        max_y = self.settings.height - 2

        dy = 1 if y == min_y else -1 if y == max_y else random.choice((1, -1))

        self.position[0] = y + dy

    def change_direction(self):
        self.direction *= -1

    def would_hit_horizontal_edge(self):
        next_x = self.position[1] + self.direction
        return (
            next_x > self.settings.width - len(self.sprite[self.direction])
            or next_x < 0
        )


class Kelp:
    """A class to store all information about a kelp."""

    def __init__(self):
        self.settings = Settings()
        self.height = random.randint(3, self.settings.height * 2 // 3)
        self.sprite = self.build_kelp()
        self.color = Colors().colors[3]
        self.position = [
            self.settings.height - 2,
            random.randint(0, self.settings.width - 2),
        ]

    def build_kelp(self):
        return [random.choice(("( ", " )")) for _ in range(self.height)]

    def sway(self):
        for i, segment in enumerate(self.sprite):
            if random.random() < 0.03:
                self.sprite[i] = " )" if segment == "( " else "( "


class Bubbler:
    """A class to store all information about a bubbler."""

    def __init__(self):
        self.settings = Settings()
        self.position = [
            self.settings.height - 1,
            random.randint(0, self.settings.width - 1),
        ]
        self.bubbles = []

    def create_bubble(self):
        if random.random() < 0.15:
            self.bubbles.append(*[self.position.copy()])

    def elevate_bubbles(self):
        if self.bubbles:
            for i, bubble in enumerate(self.bubbles):
                r = random.choice((-1, 0, 1))
                new_x = bubble[1] + r
                if 0 <= new_x <= self.settings.width - 1:
                    bubble[1] += r

                bubble[0] -= 1

                if bubble[0] < 0:
                    del self.bubbles[i]


class FishTank:
    """Overall class to manage fish_tank assets and behavior."""

    def __init__(self):
        """Initialize fish_tank and create animation resources."""
        self.settings = Settings()
        self.colors = Colors()
        self.fish_group = self.create_fish_group()
        self.kelp_group = self.create_kelp_group()
        self.bubbler_group = self.create_bubbler_group()

    def play_animation(self):
        while True:
            self.reset_grid()
            self.prep_grid()
            self.print_grid()
            self.update_assets()
            time.sleep(1 / self.settings.framerate)

    def reset_grid(self):
        self.grid = [
            [" " for _ in range(self.settings.width)]
            for _ in range(self.settings.height)
        ]

    def prep_grid(self):
        self.insert_bubblers()
        self.insert_kelp()
        self.insert_fish()
        self.insert_sand()

    def insert_kelp(self):
        reset = self.colors.reset

        for kelp in self.kelp_group:
            green = kelp.color
            for i, segment in enumerate(kelp.sprite):
                for j, char in enumerate(segment):
                    self.grid[kelp.position[0] - i][kelp.position[1] + j] = (
                        green + char + reset
                    )

    def insert_fish(self):
        reset = self.colors.reset

        for fish in self.fish_group:
            sprite = fish.sprite[fish.direction]
            color = fish.color

            for i, char in enumerate(sprite):
                self.grid[fish.position[0]][fish.position[1] + i] = color + char + reset

    def insert_sand(self):
        reset = self.colors.reset
        yellow = self.colors.colors[2]

        for i in range(self.settings.width):
            self.grid[self.settings.height - 1][i] = yellow + "░" + reset

    def insert_bubblers(self):
        for bubbler in self.bubbler_group:
            if bubbler.bubbles:
                for bubble in bubbler.bubbles:
                    self.grid[bubble[0]][bubble[1]] = random.choice(("o", "O"))

    def print_grid(self):
        print("\033[H", end="")
        for row in self.grid:
            print("".join(row), end="")
        sys.stdout.flush()

    def update_assets(self):
        self.update_fish()
        self.update_kelp()
        self.update_bubblers()

    def update_fish(self):
        for fish in self.fish_group:
            fish.swim()

    def update_kelp(self):
        for kelp in self.kelp_group:
            kelp.sway()

    def update_bubblers(self):
        for bubbler in self.bubbler_group:
            bubbler.create_bubble()
            bubbler.elevate_bubbles()

    def create_fish_group(self):
        return [Fish() for _ in range(self.settings.fish_count)]

    def create_kelp_group(self):
        return [Kelp() for _ in range(self.settings.kelp_count)]

    def create_bubbler_group(self):
        return [Bubbler() for _ in range(self.settings.bubbler_count)]


if __name__ == "__main__":
    fish_tank = FishTank()
    try:
        fish_tank.play_animation()
    except KeyboardInterrupt:
        sys.exit()
