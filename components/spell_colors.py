from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components import colors
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Castable


class SpellColor(BaseComponent):
    parent: Castable

    def __init__(self, color: Optional[color] = None):
        self.color = color

    def get_effect(self):
        raise NotImplementedError()


class Red(SpellColor):
    def __init__(self, color: colors.red):
        super().__init__(color=color)

# TODO: add effects and more spell colors
