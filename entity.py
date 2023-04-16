from __future__ import annotations

import copy
import math
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union

from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.castable import Castable
    from components.consumable import Consumable
    from components.equipment import Equipment
    from components.equippable import Equippable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from components.level import Level
    from components.spell_book import SpellBook
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory, SpellBook]

    def __init__(self,
                 parent: Optional[GameMap] = None,
                 x: int = 0,
                 y: int = 0,
                 char: str = "?",
                 codepoint: Optional[str] = "?",
                 color: Tuple[int, int, int] = (255, 255, 255),
                 name: str = "<Unnamed>",
                 blocks_movement: bool = False,
                 render_order: RenderOrder = RenderOrder.CORPSE,
                 ):
        self.x = x
        self.y = y
        self.char = char
        self.codepoint = codepoint
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if hasattr(self, "parent"):  # Possibly uninitialized
            if self.parent is self.gamemap:
                self.gamemap.entities.remove(self)
        self.parent = gamemap
        gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            codepoint: Optional[str] = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            ai_cls: Type[BaseAI],
            equipment: Equipment,
            fighter: Fighter,
            inventory: Inventory,
            spell_book: SpellBook,
            level: Level,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            codepoint=codepoint,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.spell_book = spell_book
        self.spell_book.parent = self

        self.level = level
        self.level.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)


class Item(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            codepoint: Optional[str] = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            consumable: Optional[Consumable] = None,
            equippable: Optional[Equippable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            codepoint=codepoint,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable
        if self.equippable:
            self.equippable.parent = self


class Spell(Entity):
    def __init__(
            self,
            *,
            parent: Optional[SpellBook] = None,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            codepoint: Optional[str] = "?",
            ai_cls: Type[BaseAI],
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            castable: Castable,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            codepoint=codepoint,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
            parent=parent,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)
        self.castable = castable
        if self.castable:
            self.castable.parent = self
            self.spell_power = self.castable.spell_power
            self.spell_range = self.castable.spell_range
