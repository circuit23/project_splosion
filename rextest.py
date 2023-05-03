import tcod
import numpy as np

tileset = tcod.tileset.load_tilesheet("cp437_16x16.png", 16, 16, tcod.tileset.CHARMAP_CP437)

CP437_TO_UNICODE = np.asarray(tcod.tileset.CHARMAP_CP437)
root_console, = tcod.console.load_xp("Project_Splosion_80x50.xp", order="F")
root_console.ch[:] = CP437_TO_UNICODE[root_console.ch]
KEY_COLOR = (255, 0, 255)
is_transparent = (root_console.rgb["bg"] == KEY_COLOR).all(axis=-1)
root_console.rgba[is_transparent] = (ord(" "), (0,), (0,))

with tcod.context.new_terminal(
    root_console.width,
    root_console.height,
    title="rextest",
    tileset=tileset,
    vsync=True,
) as context:
    while True:
        context.present(root_console)
        for event in tcod.event.wait():
            context.convert_event(event)
            print(event)
            if isinstance(event, tcod.event.Quit):
                raise SystemExit()

#TODO: get this integrated into the main script