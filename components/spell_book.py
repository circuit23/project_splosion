from __future__ import annotations

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Spell


class SpellBook(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.spells: List[Spell] = []

    def remove(self, spell: Spell) -> None:
        """
        Removes a spell from the spell book.
        """
        self.spells.remove(spell)

        self.engine.message_log.add_message(
            f"You removed {spell.name} from your spell book, and now it is gone to the ether."
        )
