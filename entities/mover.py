from typing import TYPE_CHECKING

from .base_entity import BaseEntity

# Mover - an entity that can move
class Mover(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy