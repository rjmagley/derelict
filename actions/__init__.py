from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple

# currently actions return a boolean to determine if the action was successful
# or not - or really, if it takes a turn or not
# there's also a lot of variety in how things are done regarding the map/engine,
# especially adding messages to the log
# this dataclass contains some key information to pass around -
# - if the action causes time to pass
# - if a message is printed as a result of the action
# - the color of the printed message
# - how long the action will take
# action time is measured in auts, stolen shamelessly from DCSS because it's
# a good term - 10 auts can be thought of as one "second"

@dataclass
class ActionResult():
    time_passed: bool = False
    message: str = ""
    message_color: Tuple[int, int, int] = (192, 192, 192)
    time_taken: int = 0