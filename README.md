# GameProject

A small Python/Pygame game project built as a learning exercise.

## Current Features

- Opens a wide 1280x720 Pygame window
- Presents a calm cinematic opening scene without enemies on screen
- Moves the player left and right slowly along the ground
- Lets the player jump with simple gravity
- Loads the background from external PNG image layers in `assets/backgrounds/`
- Draws sky, far trees, fog, mid trees, shack, and foreground as separate assets
- Uses simple parallax scrolling speeds for the image layers
- Includes temporary placeholder PNGs that can be replaced with final artwork
- Draws the player as a small cloaked silhouette with a warm lantern glow
- Keeps the older zombie, fireball, death effect, and respawn systems in the code for later combat milestones

## Background Assets

The background is loaded from these PNG files:

- `assets/backgrounds/sky.png`
- `assets/backgrounds/far_trees.png`
- `assets/backgrounds/fog.png`
- `assets/backgrounds/mid_trees.png`
- `assets/backgrounds/shack.png`
- `assets/backgrounds/foreground.png`

Replace the placeholder PNGs with final art using the same filenames. Transparent layers should be saved as PNGs with alpha.

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
