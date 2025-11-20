import shutil


class Settings:
    """A class to store all settings for fish_tank."""

    def __init__(self):
        self.size = shutil.get_terminal_size()
        self.width = self.size.columns
        self.height = self.size.lines


class Fish:
    """A class to store all information about the fish."""

    FISH_TYPES = [
        {
            "right": r"""
                \'`.
                 )  \
    (`.??????_.-`' ' '`-.
     \ `.??.`        (o) \_
      >  ><     (((       (
     / .`??`._      /_|  /'
    (.`???????`-. _  _.-`
                /__/'
    """,
            "left": r"""
           .'`/
          /  (
      .-'` ` `'-._??????.')
    _/ (o)        '.??.' /
    )       )))     ><  <
    `\  |_\      _.'??'. \
      '-._  _ .-'???????'.)
          `\__\
    """,
        }
    ]

    def __init__(self):
        pass


class FishTank:
    """Overall class to manage fish_tank assets and behavior."""

    def __init__(self):
        """Initialize fish_tank and create animation resources"""
        self.settings = Settings()
        self.fish = Fish()

    def play_animation(self):
        while True:
            pass


if __name__ == "__main__":
    fish_tank = FishTank()
    fish_tank.play_animation()
