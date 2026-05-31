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

# Enemy health
enemy_health = 3
enemy_max_health = 3

# Enemy speech text
enemy_text = ""

# How many frames the text should remain visible
enemy_text_timer = 0

# Has the enemy finished dying?
enemy_dead = False

# Tracks whether the left mouse button was clicked this frame
mouse_clicked = False

collision_active = False

# Create a clock to control the frame rate
clock = pygame.time.Clock()

# Main game loop
# This will continue running until running becomes False
while running:
    
    # Reset mouse click each frame
    mouse_clicked = False

    # Check for events (keyboard, mouse, window close, etc.)
    for event in pygame.event.get():

        # Check for left mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
        # Check if the player clicked the X button
        elif event.type == pygame.QUIT:

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

        # If the player clicks while touching the enemy and enemy is still alive.
        if mouse_clicked and enemy_health > 0:
            enemy_health -= 1
            enemy_health = max(enemy_health, 0)
            
            if enemy_health == 2:
                enemy_text = "???"
            elif enemy_health == 1:
                enemy_text = "OUCH!!"
            elif enemy_health == 0:
                enemy_text = "Ugh... I'm defeated..."
            enemy_text_timer = 60

            print(f"Enemy health: {enemy_health}")

        collision_active = True

    else:
        collision_active = False

    # Count down the enemy text timer
    if enemy_text_timer > 0:
        enemy_text_timer -= 1

    # Once the death message finishes, mark the enemy as fully dead
    if enemy_text_timer == 0 and enemy_health == 0:
        enemy_dead = True

    # Draw the frame
    screen.fill((30, 30, 30))

    # Draw the player
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (player_x, player_y, player_size, player_size)
    )

    
    # Draw the enemy
    if enemy_dead:
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (enemy_x, enemy_y, enemy_size, enemy_size)
        )

        # Draw death marker
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (enemy_x + 10, enemy_y + 10),
            (enemy_x + 40, enemy_y + 40),
            3
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (enemy_x + 40, enemy_y + 10),
            (enemy_x + 10, enemy_y + 40),
            3
        )

    else:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (enemy_x, enemy_y, enemy_size, enemy_size)
        )

    # Draw skull when enemy is dead
    if enemy_health == 0:

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (enemy_x + 10, enemy_y + 10),
            (enemy_x + 40, enemy_y + 40),
            3
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (enemy_x + 40, enemy_y + 10),
            (enemy_x + 10, enemy_y + 40),
            3
        )

    # Enemy health bar background
    
    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (enemy_x, enemy_y - 15, enemy_size, 8)
    )

    # Enemy health bar fill
    health_ratio = enemy_health / enemy_max_health
    health_bar_width = enemy_size * health_ratio

    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (enemy_x, enemy_y - 15, health_bar_width, 8)
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
