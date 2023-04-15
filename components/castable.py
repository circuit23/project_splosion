from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.ai
import components.spell_book
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import AreaRangedAttackHandler, SingleRangedAttackHandler

if TYPE_CHECKING:
    from entity import Actor, Spell


class Castable(BaseComponent):
    parent: Spell

    def __init__(self, spell_power: int = 0, spell_range: int = 0):
        self.spell_power = spell_power
        self.spell_range = spell_range

    def get_action(self, consumer: Actor):
        """Try to return the action for this spell."""
        return actions.SpellAction(consumer, self.parent)

    def cast(self, action: actions.SpellAction) -> None:
        """Invoke this spell's effect.

        'action' is the context for this activation.
        """
        raise NotImplementedError()

    def remove(self) -> None:
        """Remove this spell from the spell book."""
        entity = self.parent
        spell_book = entity.parent
        if isinstance(spell_book, components.spell_book.SpellBook):
            spell_book.spells.remove(entity)


class BasicSpell(Castable):
    def __init__(self, spell_power: int, spell_range: int) -> None:
        self.spell_power = spell_power
        self.spell_range = spell_range
        super().__init__(self.spell_power, self.spell_range)

    def get_action(self, consumer: Actor) -> SingleRangedAttackHandler:
        self.engine.message_log.add_message(
            "Oh shit, a spell. Select a target location.", color.needs_target
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
            f"You cast the basic spell at the {target.name}. A bolt of pure magic streaks out at them!",
            color.status_effect_applied
        )
        target.fighter.hp -= self.spell_power
