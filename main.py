#!/usr/bin/env python3
import traceback

import tcod

from components.tileset import tile_set
from components import colors
import exceptions
import input_handlers
import setup_game


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

# TODO: create an item factory system similar to entity_factory
# TODO: create an ELABORATE spell factory system similar to entity_factory, with colors, etc
# TODO: once some spells are working, start ASCII animations
# TODO: figure out how to make the loading screen look like it really looks full-size
# TODO: give the Arena its own savegame so it doesn't keep overwriting the other one
# TODO: make the console area resizable like in the scratch example
# TODO: bigger, scrollable/lookable GameMaps


def main() -> None:
    screen_width = 80
    screen_height = 50

    tileset = tile_set()

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
                            traceback.format_exc(), colors.error
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
