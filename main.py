#!/usr/bin/env python3
import traceback

import tcod

import color
import exceptions
import input_handlers
import setup_game


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tcod.tileset.load_tilesheet(
        "TiledFont.png", 32, 10, tcod.tileset.CHARMAP_TCOD
    )
    tileset.remap(0x100000, 2, 5)  # Assign codepoint 0x100000 to a character sprite
    tileset.remap(0x100001, 3, 5)  # Orcs
    tileset.remap(0x100002, 4, 5)  # Trolls
    tileset.remap(0x100003, 5, 5)  # Scrolls
    tileset.remap(0x100004, 6, 5)  # Potions
    tileset.remap(0x100005, 7, 5)  # sword
    tileset.remap(0x100008, 10, 5)  # dagger
    tileset.remap(0x100006, 8, 5)  # armor
    tileset.remap(0x100007, 9, 5)  # downstairs
    tileset.remap(0x100009, 0, 5)  # wall
    tileset.remap(0x100010, 1, 5)  # floor

    # TODO: put tileset stuff in better place (maybe components?) instead of main
    # TODO: figure out FOV/visible vs explored tweaks now that i'm using the new sprites
    # TODO: make the console area resizable like in the scratch example

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="PROJECT SPLOSION!",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and exit
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise


if __name__ == '__main__':
    main()
