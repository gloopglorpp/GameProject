# Background Assets

The game loads these PNG files in order:

- `sky.png` placeholder
- `far_trees.png` placeholder
- `fog.png` placeholder
- `mid_trees.png` real imported forest art
- `shack.png` real imported shack art, converted to transparency from a checkerboard source
- `foreground.png` real imported foreground art

Replace any placeholder PNGs with final artwork when ready. Transparent layers should be saved as PNGs with alpha, and the code will scale layers to fit the 1280x720 window if needed.
