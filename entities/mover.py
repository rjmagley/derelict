from typing import TYPE_CHECKING

from .base_entity import BaseEntity

# Mover - an entity that can move
class Mover(BaseEntity):
    def __init__(self, move_speed: int = 10, **kwargs):
        super().__init__(**kwargs)
        # delay is a measure of how many auts until something can act again
        # when a creature's delay is 0 or less, it acts
        self.delay = 10
        # an entity is "awake" if it needs to act - this will cut down on some
        # of the checks that have to be made later
        self.awake = False
        self.move_speed = move_speed

    @property
    def is_alive(self) -> bool:
        return False

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy