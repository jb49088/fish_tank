import shutil

SIZE = shutil.get_terminal_size()
WIDTH = SIZE.columns
HEIGHT = SIZE.lines

FISH_TYPES = {
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
