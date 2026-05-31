# Import the pygame library
import pygame

# Initialize all pygame modules
# This must be called before using most pygame features
pygame.init()

# Screen size
screen_width = 800
screen_height = 600

# Create a game window
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title shown at the top of the window
pygame.display.set_caption("My Game")

# Create a font for drawing text on the screen
font = pygame.font.Font(None, 36)

# Create a variable that controls whether the game is running
running = True

# Player position
player_x = 100
player_y = 100

# Player size
player_size = 50

# How many pixels the player moves each frame
player_speed = 5

# Enemy position
enemy_x = 500
enemy_y = 300

# Enemy size
enemy_size = 50

# Enemy speech text
enemy_text = ""

# How many frames the text should remain visible
enemy_text_timer = 0

collision_active = False

# Create a clock to control the frame rate
clock = pygame.time.Clock()

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

    # Prevent the player from leaving the screen

    if player_x < 0:
        player_x = 0

    if player_y < 0:
        player_y = 0

    if player_x > screen_width - player_size:
        player_x = screen_width - player_size

    if player_y > screen_height - player_size:
        player_y = screen_height - player_size

    # Create rectangles for collision detection
    player_rect = pygame.Rect(
        player_x,
        player_y,
        player_size,
        player_size
    )

    enemy_rect = pygame.Rect(
        enemy_x,
        enemy_y,
        enemy_size,
        enemy_size
    )

    # Check if player and enemy are touching
    if player_rect.colliderect(enemy_rect):
        if not collision_active:
            enemy_text = "Hmm..."
            enemy_text_timer = 60 # Show text for 60 frames (1 second at 60 FPS)
            collision_active = True
    else:
        collision_active = False

    # Count down the enemy text timer
    if enemy_text_timer > 0:
        enemy_text_timer -= 1

    # Draw the frame
    screen.fill((30, 30, 30))

    # Draw the player
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (player_x, player_y, player_size, player_size)
    )

    # Draw the enemy
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (enemy_x, enemy_y, enemy_size, enemy_size)
    )

    # Draw enemy text if the timer is active
    if enemy_text_timer > 0:
        text_surface = font.render(enemy_text, True, (255, 255, 255))

        screen.blit(
            text_surface,
            (enemy_x, enemy_y - 40)
        )
    pygame.display.flip()
    # Limit the game to 60 frames per second
    clock.tick(60)

# Quit pygame and clean up resources
pygame.quit()
