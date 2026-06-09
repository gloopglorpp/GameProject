import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_COLOR = (35, 46, 42)

ENEMY_SIZE = 50
ENEMY_COLOR = (64, 48, 46)
ENEMY_DEFEATED_COLOR = (105, 105, 105)

GROUND_Y = 485

SKY_COLOR = (146, 177, 193)
MOUNTAIN_FAR_COLOR = (96, 113, 123, 95)
MOUNTAIN_NEAR_COLOR = (72, 88, 91, 130)
GRASS_COLOR = (86, 122, 74)
GROUND_COLOR = (51, 65, 54)
GROUND_SHADOW_COLOR = (35, 42, 36)
TEXT_COLOR = (235, 238, 245)
MUTED_TEXT_COLOR = (155, 165, 180)


def draw_text(screen, font, text, x, y, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_mountains(screen, points, color):
    mountain_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(mountain_layer, color, points)
    screen.blit(mountain_layer, (0, 0))


def draw_background(screen):
    screen.fill(SKY_COLOR)

    draw_mountains(
        screen,
        [
            (0, GROUND_Y),
            (0, 250),
            (120, 170),
            (260, 285),
            (390, 155),
            (570, 305),
            (700, 205),
            (SCREEN_WIDTH, 270),
            (SCREEN_WIDTH, GROUND_Y),
        ],
        MOUNTAIN_FAR_COLOR,
    )

    draw_mountains(
        screen,
        [
            (0, GROUND_Y),
            (0, 335),
            (110, 260),
            (210, 345),
            (340, 235),
            (475, 355),
            (615, 245),
            (SCREEN_WIDTH, 350),
            (SCREEN_WIDTH, GROUND_Y),
        ],
        MOUNTAIN_NEAR_COLOR,
    )

    pygame.draw.rect(screen, GRASS_COLOR, (0, GROUND_Y, SCREEN_WIDTH, 18))
    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y + 18, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
    pygame.draw.rect(screen, GROUND_SHADOW_COLOR, (0, GROUND_Y + 50, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))


def draw_enemy(screen, enemy_rect, enemy_health, enemy_max_health):
    if enemy_health > 0:
        pygame.draw.rect(screen, ENEMY_COLOR, enemy_rect, border_radius=6)
    else:
        pygame.draw.rect(screen, ENEMY_DEFEATED_COLOR, enemy_rect, border_radius=6)

        pygame.draw.line(
            screen,
            TEXT_COLOR,
            (enemy_rect.x + 12, enemy_rect.y + 12),
            (enemy_rect.x + ENEMY_SIZE - 12, enemy_rect.y + ENEMY_SIZE - 12),
            3,
        )
        pygame.draw.line(
            screen,
            TEXT_COLOR,
            (enemy_rect.x + ENEMY_SIZE - 12, enemy_rect.y + 12),
            (enemy_rect.x + 12, enemy_rect.y + ENEMY_SIZE - 12),
            3,
        )

    health_bar_width = ENEMY_SIZE
    pygame.draw.rect(
        screen,
        (80, 85, 95),
        (enemy_rect.x, enemy_rect.y - 15, health_bar_width, 8),
        border_radius=3,
    )

    health_ratio = enemy_health / enemy_max_health
    pygame.draw.rect(
        screen,
        (95, 215, 105),
        (enemy_rect.x, enemy_rect.y - 15, health_bar_width * health_ratio, 8),
        border_radius=3,
    )


def run_game(max_frames=None):
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("GameProject")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)

    player_rect = pygame.Rect(100, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
    enemy_rect = pygame.Rect(500, GROUND_Y - ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)

    enemy_max_health = 3
    enemy_health = enemy_max_health
    enemy_text = ""
    enemy_text_timer = 0
    frames_run = 0
    running = True

    while running:
        attack_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    attack_pressed = True
                elif event.key == pygame.K_r and enemy_health == 0:
                    enemy_health = enemy_max_health
                    enemy_text = "Back for more!"
                    enemy_text_timer = 60
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                attack_pressed = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_d]:
            player_rect.x += PLAYER_SPEED
        player_rect.clamp_ip(screen.get_rect())
        player_rect.bottom = GROUND_Y

        touching_enemy = player_rect.colliderect(enemy_rect)
        if attack_pressed and touching_enemy and enemy_health > 0:
            enemy_health = max(enemy_health - 1, 0)

            if enemy_health == 2:
                enemy_text = "???"
            elif enemy_health == 1:
                enemy_text = "OUCH!!"
            else:
                enemy_text = "Defeated!"

            enemy_text_timer = 60

        if enemy_text_timer > 0:
            enemy_text_timer -= 1

        draw_background(screen)

        pygame.draw.rect(screen, PLAYER_COLOR, player_rect, border_radius=6)
        draw_enemy(screen, enemy_rect, enemy_health, enemy_max_health)

        if enemy_text_timer > 0:
            draw_text(screen, font, enemy_text, enemy_rect.x, enemy_rect.y - 45)

        draw_text(screen, small_font, "A/D move", 20, 20, MUTED_TEXT_COLOR)
        draw_text(screen, small_font, "Space/click attack while touching", 20, 45, MUTED_TEXT_COLOR)

        if enemy_health == 0:
            draw_text(screen, small_font, "Press R to respawn the enemy", 20, 70, MUTED_TEXT_COLOR)

        pygame.display.flip()
        clock.tick(FPS)

        frames_run += 1
        if max_frames is not None and frames_run >= max_frames:
            running = False

    pygame.quit()


if __name__ == "__main__":
    run_game()
