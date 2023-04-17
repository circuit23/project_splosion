from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

import actions
from components import colors
import components.ai
import components.spell_book
from components.base_component import BaseComponent
from components.spell_colors import SpellColor
from exceptions import Impossible
from input_handlers import SingleRangedAttackHandler

if TYPE_CHECKING:
    from entity import Actor, Spell


class Castable(BaseComponent):
    """Basic component of a spell that makes it castable."""
    parent: Spell

    def get_action(self, consumer: Actor):
        """Try to return the action for this spell."""
        return actions.SpellAction(consumer, self.parent)

    def cast(self, action: actions.SpellAction) -> None:
        """Invoke this spell's effect.

        'action' is the context for this activation.
        """
        raise NotImplementedError()


class SpellStructure(Castable):
    """Basic spell structure to be built up to the final spell.
    A Speleton, if you will.
    """
    def __init__(
            self,
            spell_power: int = 0,
            spell_range: int = 0,
            spell_colors: Optional[List[SpellColor]] = None,
    ) -> None:
        self.spell_power = spell_power
        self.spell_range = spell_range
        self.spell_colors = spell_colors

    def cast(self, action: actions.SpellAction) -> None:
        """Return the effects of casting this spell with all the colors."""
        # TODO: implement these effects as part of spell_colors- for each color, get effect, then apply
        raise NotImplementedError()

    def remove(self) -> None:
        """Remove this spell from the spell book."""
        entity = self.parent
        spell_book = entity.parent
        if isinstance(spell_book, components.spell_book.SpellBook):
            spell_book.spells.remove(entity)


class BasicSpell(SpellStructure):
    """Basic colorless spell for initial testing."""
    def get_action(self, consumer: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Oh shit, a spell. Select a target location.", colors.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.SpellAction(consumer, self.parent, xy),
        )

    def cast(self, action: actions.SpellAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise Impossible("You must select a valid target.")
        if consumer.distance(target.x, target.y) > self.spell_range:
            raise Impossible("You must cast the spell within its range.")

        self.engine.message_log.add_message(
            # TODO: make this message change based on what type of spell you're casting, etc
            f"Player sends a bolt of pure magic at the {target.name}, for {self.spell_power} damage.",
            colors.status_effect_applied
        )
        target.fighter.hp -= self.spell_power
