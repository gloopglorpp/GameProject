# GameProject

A small Python/Pygame game project built as a learning exercise.

## Current Features

- Opens a wide 1280x720 Pygame window
- Presents a calm cinematic opening scene without enemies on screen
- Uses `assets/backgrounds/sky.png` as the single full-screen background image
- Places the player on the black grass line inside the background artwork
- Lets the player walk directly across the screen in the opening scene
- Lets the player jump with simple gravity
- Draws the player as a small cloaked silhouette with a warm lantern glow
- Adds a small group of amber fireflies that orbit, follow, pulse, and dart around the player
- Keeps the older zombie, fireball, death effect, and respawn systems in the code for later combat milestones

## Background Assets

The active background is:

- `assets/backgrounds/sky.png`

The image already includes the sunset, distant landscape, and black grass foreground. Replace this file with another same-style PNG if you want to change the full scene.

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
