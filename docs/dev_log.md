2026-05-30

- Created initial project structure and planning documents
- Defined game concept and first development tasks
- Installed and configured VS Code
- Ran first Python program successfully
- Learned variables, user input, and type conversion
- Learned how Python imports work across multiple files
- Created player, enemy, and combat modules
- Built first text-based combat prototype
- Added player XP progression
- Created reusable attack function
- Built first combat loop
- Installed Pygame
- Created first game window
- Learned the basics of the game loop and rendering
- Drew first object on screen
- Added WASD movement controls
- Learned Pygame coordinate system
- Added player movement boundaries
- Learned how coordinate constraints keep game objects inside the world
- Replaced hardcoded boundary values with reusable screen and player size variables
- Learned why "magic numbers" can make code harder to maintain
- Set up Git repository
- Connected project to GitHub
- Added .gitignore and cleaned repository files
- Started development journal

- Added first enemy object to the game world
- Introduced enemy position and size variables
- Rendered multiple game objects on screen simultaneously
- Debugged duplicate rendering code causing enemy flickering
- Learned the importance of drawing objects once per frame
- Learned the correct render order: clear screen → draw objects → update display
- Created rectangle objects for collision detection
- Learned how game objects can be represented as collision boxes
- Implemented collision detection using Pygame's colliderect() method
- Detected when the player and enemy overlap
- Learned the difference between object positions and object boundaries
- Learned how object-oriented methods can be called on Pygame objects
- Fixed repeated collision messages by introducing collision state tracking
- Learned the difference between continuous collision detection and one-time collision events
- Learned how game loops repeatedly evaluate conditions every frame
- Added temporary enemy dialogue system
- Displayed text above game objects using Pygame fonts
- Introduced timer-based events
- Learned how frame-based timers work
- Added a game clock using pygame.time.Clock()
- Limited the game to 60 frames per second
- Learned why game speed should not depend on computer performance
- Added enemy health system
- Implemented mouse-click attacks
- Connected combat to collision detection
- Added visual enemy health bar
- Introduced enemy maximum health tracking
- Added enemy death state
- Created visual death indicators for defeated enemies
- Added state-based enemy dialogue reactions
- Learned how game objects transition between alive and dead states
- Implemented delayed death effects using timers

2026-06-09

- Reconnected the project entry point to the Pygame version of the game
- Replaced the old terminal combat startup with the visual game loop
- Moved the Pygame loop into a reusable run_game() function
- Kept game startup protected with an if __name__ == "__main__" check
- Added Space key attacks alongside left mouse click attacks
- Added Escape key support for quitting the game
- Added R key support for respawning a defeated enemy
- Added small on-screen control hints
- Cleaned up repeated enemy death drawing logic
- Updated README controls and run instructions
- Updated the task list to show completed enemy combat milestones
- Verified the project with Python compile and Pygame startup checks

- Added a simple coloured sky background
- Added faded mountain layers to create distance and setting
- Added a grass and ground strip
- Introduced a reusable GROUND_Y value
- Positioned the player and enemy so their feet sit on the ground
- Changed player movement from free movement to left/right ground movement
- Learned how background layers can suggest atmosphere before adding detailed art assets

- Added a basic jump using upward velocity and gravity
- Kept the player landing on the shared ground line
- Changed Escape from quitting immediately to opening a pause menu
- Added Resume, Controls, and Quit pause menu options
- Added keyboard navigation for the pause menu
- Added mouse clicking for pause menu buttons
- Moved gameplay controls off the main screen and into the Controls menu
- Learned how a game state can pause gameplay updates while still drawing the scene

- Changed jump from W/Up to Space
- Kept enemy attacks on left mouse click only
- Kept Enter and mouse click as pause menu selection controls
- Updated the controls menu and README to match the new input layout

- Added mouse hover highlighting for pause menu options
- Reused the selected pause option for both keyboard and mouse navigation

- Added a simple sword blade and hilt to the player
- Tracked which direction the player is facing
- Made the sword switch sides when the player moves left or right
- Changed enemy hit detection to use sword range instead of player body overlap
- Updated controls and docs to describe sword attacks

- Replaced the player square with a simple stick figure silhouette
- Drew the player using a head circle and line-based body parts
- Kept the existing player collision rectangle for movement and combat
- Reattached the sword to the stick figure's front hand
- Learned how visual drawing can change without changing the underlying hitbox

- Added a world_x value to track progress through the world
- Kept the player near a fixed screen position while the world moves
- Made the enemy use a world position so it appears as the player progresses
- Added moving cloud layers for atmosphere
- Added background_time so parts of the background move even while standing still
- Added parallax mountain movement for background depth
- Added repeating grass highlights to make the ground feel alive
- Learned the difference between screen position and world position

- Added a walking animation frame for the player silhouette
- Used a sine wave to swing the player's arms and legs while moving
- Added a small body bounce during walking
- Added a separate jumping pose for the player silhouette
- Kept the player hitbox unchanged while animating the drawing

- Removed the visible sword from the player
- Added a short punch range in front of the player
- Changed left click from sword attack to punch attack
- Drew a small fist on the front hand of the stick figure
- Kept direction-based attack collision using a punch rectangle

- Turned the player silhouette into a small blue wizard
- Added a robe, pointed hat, sparkles, and wooden staff
- Replaced punch attacks with staff-cast fireballs
- Added fireball projectiles with glow, core, edge, and trail drawing
- Made fireballs move through world space and collide with enemies
- Updated controls and docs to describe fireball casting

- Removed floating enemy dialogue text from combat
- Replaced the block enemy with a simple zombie character drawing
- Added zombie skin, clothing, face, arms, and leg details
- Made the zombie slowly move toward the player's world position
- Kept the enemy health bar as the main combat feedback
- Reset the zombie ahead of the player when respawned

- Added varied zombie death effects using flame and smoke particles
- Created multiple death effect patterns so defeats do not look identical
- Made particles rise, fade, shrink, or expand over time
- Removed the manual R respawn control
- Added automatic zombie respawn after the death effect clears
- Respawned zombies off-screen ahead of the player to avoid visible pop-in

2026-06-10

- Replaced the simple blue sky and mountain background with a warm nostalgic silhouette scene
- Added a sunset-style gradient sky and soft pulsing glow for atmosphere
- Added layered parallax hills to create a stronger sense of distance
- Added drifting mist bands so the background feels softer and deeper
- Added a large tree silhouette with branches and a gently swaying rope swing
- Added an abandoned shack silhouette as a repeating background landmark
- Added small firefly-like glowing particles for warm ambient motion
- Added a dark foreground ridge, richer grass strokes, and vignette framing
- Kept the wizard, zombie, fireball, and respawn gameplay unchanged while improving the art direction
- Learned how multiple simple transparent layers can create a more detailed scene without importing art assets

- Widened the game window from 800x600 to 1280x720 for a more cinematic view
- Slowed player movement so the player has more time to take in the scene
- Added an opening scene mode that hides enemies, fireballs, and combat effects for now
- Reworked the forest into a denser composition with distant trunks, heavy canopy, and stronger silhouettes
- Enlarged the tree into a foreground landmark with roots, thick branches, and a hanging swing
- Expanded the abandoned shack with a larger broken shape, lit window, planks, and fence pieces
- Changed the player from a bright wizard into a small cloaked silhouette with a warm lantern glow
- Updated the controls menu and README to match the quieter opening scene
- Learned how temporarily gating systems can let one milestone focus on art direction without deleting earlier gameplay work

- Created an `assets/backgrounds/` folder for external background PNG files
- Added placeholder PNGs for sky, far trees, fog, mid trees, shack, and foreground
- Replaced procedural scenery drawing with an asset-based background layer system
- Loaded PNG layers with `pygame.image.load().convert_alpha()`
- Added scaling so background images can fit the current game window
- Added parallax layer speeds so sky stays still while foreground moves fastest
- Kept player, collision, enemy, and combat code separate from background art
- Added asset README notes explaining which PNG files can be replaced later
- Learned why art assets should live outside gameplay code once the visual direction becomes more serious

- Replaced the placeholder `mid_trees.png`, `shack.png`, and `foreground.png` files with imported artwork
- Converted the shack file's checkerboard background into transparency so it behaves like a proper PNG overlay
- Added per-layer scaling metadata so the shack can be drawn as a smaller scene object
- Kept the existing image-layer background order and parallax system intact
- Left `sky.png`, `far_trees.png`, and `fog.png` as temporary placeholders until final art is available
- Verified the real PNG layers load through the existing Pygame asset pipeline

- Replaced the active background with the supplied `sky.png` sunset artwork
- Changed the background layer spec so only `sky.png` is drawn for the opening scene
- Moved `GROUND_Y` down to the black grass line in the new artwork
- Changed opening-scene movement so the player walks across the screen instead of staying fixed while the world scrolls
- Kept enemies, fireballs, and older background assets inactive for the quiet opening scene
- Updated README, tasks, and background asset notes to describe the single-image setup

- Added a small group of 3-6 amber fireflies that stay near the player instead of spawning across the scene
- Used the player rectangle to calculate a target point around the character's head
- Gave each firefly its own orbit angle, radius, speed, jitter, pulse, and follow strength
- Added occasional dart behavior so fireflies sometimes zip toward the head or back away
- Drew each firefly with a soft amber glow and bright core
- Kept the firefly system separate from background art and collision logic
