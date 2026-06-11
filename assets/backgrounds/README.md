# Background Assets

The current opening scene uses one wide background image:

- `area_01_forest.png` (12000x2000)

`src/game.py` draws a 1920x1080 camera crop from this image. The player stores a world x-position, and the camera follows that position while staying inside the image boundaries.

The vertical crop is controlled by `BACKGROUND_VIEW_Y` so the black grass in the artwork lines up with the playable ground line.

Earlier layered background PNGs were removed for this pass so the scene is driven by one finished artwork strip.
