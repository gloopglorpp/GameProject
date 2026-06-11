# GameProject

A small Python/Pygame game project built as a learning exercise.

## Current Features

- Opens a cinematic 1920x1080 Pygame window
- Uses one wide `assets/backgrounds/area_01_forest.png` image as the opening-area background
- Crops the 12000x2000 artwork into a 1920x1080 camera view
- Spawns the player in the centre of the screen
- Keeps the camera focused on the player as they move through the wide scene
- Places the player on the black grass line inside the background artwork
- Lets the player walk slowly and jump with simple gravity
- Draws the player as a small cloaked silhouette with a warm lantern glow
- Keeps the older zombie, fireball, death effect, and respawn systems in the code for later combat milestones

## Background Assets

The active opening background is:

- `assets/backgrounds/area_01_forest.png`

The image is a wide 12000x2000 artwork strip. The game draws a 1920x1080 crop from it and moves that crop as the player walks, creating a camera-follow effect without rebuilding the background from shapes.

## Controls

- A = slow walk left
- D = slow walk right
- Space = jump
- Esc = pause menu

## Pause Menu

The pause menu has Resume, Controls, and Quit options. Use W/S or Up/Down to choose an option, then press Enter. You can also click menu buttons with the mouse.

## Run

```bash
python3 src/main.py
```

## Goal

Build a simple 2D game step by step, balancing playable systems with a strong, atmospheric world.
