from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Castable, Spell


class SpellColor(BaseComponent):
    parent: Castable

    def __init__(self, color: Optional[str] = None):
        self.color = color

    def get_effect(self):
        raise NotImplementedError()
