"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
import spell_factory
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("Project_Splosion_small.png")[:, :, :3]


def arena_game() -> Engine:
    """Return an arena session as an Engine instance."""
    map_width = 80
    map_height = 43

    # Leave in useless numbers so they don't cause errors
    room_max_size = 80
    room_min_size = 6
    max_rooms = 30

    fov_radius: int = 80

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        fov_radius=fov_radius,
    )

    engine.game_world.generate_arena_floor()
    engine.update_fov(fov_radius)

    engine.message_log.add_message(
        "Welcome to the Arena! Prepare to die in a splosion!!", color.welcome_text
    )

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)
    basic_spell = copy.deepcopy(spell_factory.basic_spell)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory
    basic_spell.parent = player.spell_book

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    player.spell_book.spells.append(basic_spell)

    return engine


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", color.welcome_text
    )

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)
    basic_spell = copy.deepcopy(spell_factory.basic_spell)


    dagger.parent = player.inventory
    leather_armor.parent = player.inventory
    basic_spell.parent = player.spell_book

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    player.spell_book.spells.append(basic_spell)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 4 * 3,
            console.height // 2 - 20,
            "PROJECT SPLOSION!",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width - 8,
            console.height - 2,
            "By Circuit 23",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[A] Arena for testing", "[Q] Quit"]
        ):
            console.print(
                console.width // 4 * 3,
                console.height // 2 - 18 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())
        elif event.sym == tcod.event.K_a:
            return input_handlers.ArenaEventHandler(arena_game())

        return None
