# Import the pygame library
import pygame

# Initialize all pygame modules
# This must be called before using most pygame features
pygame.init()

# Create a game window
# (800, 600) means 800 pixels wide and 600 pixels tall
screen = pygame.display.set_mode((800, 600))

# Set the title shown at the top of the window
pygame.display.set_caption("My Game")

# Create a variable that controls whether the game is running
running = True

# Player position
player_x = 100
player_y = 100

# How many pixels the player moves each frame
player_speed = 5

# Main game loop
# This will continue running until running becomes False
while running:

    # Check for events (keyboard, mouse, window close, etc.)
    for event in pygame.event.get():

        # Check if the player clicked the X button
        if event.type == pygame.QUIT:

            # Stop the game loop
            running = False

    # Check which keys are currently being held down
    keys = pygame.key.get_pressed()

    # Move left (A)
    if keys[pygame.K_a]:
        player_x -= player_speed

    # Move right (D)
    if keys[pygame.K_d]:
        player_x += player_speed

    # Move up (W)
    if keys[pygame.K_w]:
        player_y -= player_speed

    # Move down (S)
    if keys[pygame.K_s]:
        player_y += player_speed

    # Fill the entire screen with a dark grey color
    #
    # RGB values:
    # Red   = 30
    # Green = 30
    # Blue  = 30
    #
    # (0, 0, 0) = black
    # (255, 255, 255) = white
    screen.fill((30, 30, 30))

    # Draw a green rectangle
    #
    # Parameters:
    # screen       = where to draw
    # (0,255,0)    = green color (RGB)
    # (100,100)    = x,y position
    # (50,50)      = width,height
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (player_x, player_y, 50, 50)
    )

    # Update the display so any changes become visible
    pygame.display.flip()

# Shut down pygame cleanly after the loop ends
pygame.quit()