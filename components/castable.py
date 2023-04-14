from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.spell_book
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import ActionOrHandler, AreaRangedAttackHandler

if TYPE_CHECKING:
    from entity import Actor, Spell


class Castable(BaseComponent):
    parent: Spell

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this spell."""
        return actions.SpellAction(consumer, self.parent)

    def cast(self, action: actions.SpellAction) -> None:
        """Invoke this spell's ability.
        'action' is the context for this activation.
        """
        raise NotImplementedError()

    def remove(self) -> None:
        """Remove the spell from spell book."""
        entity = self.parent
        spell_book = entity.parent
        if isinstance(spell_book, components.spell_book.SpellBook):
            spell_book.spells.remove(entity)

# TODO: add in some simple spells to test with
# TODO: add in ranged targeting for them
