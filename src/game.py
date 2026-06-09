import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_SIZE = 50
PLAYER_SPEED = 5
JUMP_STRENGTH = -16
GRAVITY = 1
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
MENU_OVERLAY_COLOR = (12, 16, 18, 175)
MENU_PANEL_COLOR = (34, 42, 43)
MENU_SELECTED_COLOR = (92, 121, 105)
PAUSE_OPTIONS = ["Resume", "Controls", "Quit"]


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


def get_pause_buttons():
    buttons = []
    for index, label in enumerate(PAUSE_OPTIONS):
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 110, 245 + index * 65, 220, 45)
        buttons.append((label, rect))
    return buttons


def get_controls_back_button():
    return pygame.Rect(SCREEN_WIDTH // 2 - 110, 420, 220, 45)


def draw_menu_button(screen, font, text, rect, selected=False):
    color = MENU_SELECTED_COLOR if selected else MENU_PANEL_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, TEXT_COLOR, rect, 2, border_radius=6)

    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_pause_menu(screen, title_font, button_font, selected_option):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(MENU_OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))

    title_surface = title_font.render("Paused", True, TEXT_COLOR)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 180))
    screen.blit(title_surface, title_rect)

    buttons = get_pause_buttons()
    for index, (label, rect) in enumerate(buttons):
        draw_menu_button(screen, button_font, label, rect, selected_option == index)

    return buttons


def draw_controls_menu(screen, title_font, button_font, small_font):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill(MENU_OVERLAY_COLOR)
    screen.blit(overlay, (0, 0))

    title_surface = title_font.render("Controls", True, TEXT_COLOR)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
    screen.blit(title_surface, title_rect)

    controls = [
        "A / D: move",
        "W / Up: jump",
        "Space / left click: attack while touching enemy",
        "R: respawn defeated enemy",
        "Esc: pause or return",
    ]

    for index, line in enumerate(controls):
        text_surface = small_font.render(line, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 220 + index * 32))
        screen.blit(text_surface, text_rect)

    back_rect = get_controls_back_button()
    draw_menu_button(screen, button_font, "Back", back_rect, True)
    return back_rect


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
    title_font = pygame.font.Font(None, 56)
    small_font = pygame.font.Font(None, 24)

    player_rect = pygame.Rect(100, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
    enemy_rect = pygame.Rect(500, GROUND_Y - ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)

    enemy_max_health = 3
    enemy_health = enemy_max_health
    enemy_text = ""
    enemy_text_timer = 0
    player_y_velocity = 0
    selected_pause_option = 0
    game_state = "playing"
    frames_run = 0
    running = True

    while running:
        attack_pressed = False
        jump_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "paused"
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        jump_pressed = True
                    elif event.key == pygame.K_SPACE:
                        attack_pressed = True
                    elif event.key == pygame.K_r and enemy_health == 0:
                        enemy_health = enemy_max_health
                        enemy_text = "Back for more!"
                        enemy_text_timer = 60
                elif game_state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "playing"
                    elif event.key in (pygame.K_w, pygame.K_UP):
                        selected_pause_option = (selected_pause_option - 1) % 3
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        selected_pause_option = (selected_pause_option + 1) % 3
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if selected_pause_option == 0:
                            game_state = "playing"
                        elif selected_pause_option == 1:
                            game_state = "controls"
                        else:
                            running = False
                elif game_state == "controls":
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                        game_state = "paused"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "playing":
                    attack_pressed = True
                elif game_state == "paused":
                    for index, (_, rect) in enumerate(get_pause_buttons()):
                        if rect.collidepoint(event.pos):
                            if index == 0:
                                game_state = "playing"
                            elif index == 1:
                                game_state = "controls"
                            else:
                                running = False
                elif game_state == "controls":
                    if get_controls_back_button().collidepoint(event.pos):
                        game_state = "paused"

        if game_state == "playing":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                player_rect.x -= PLAYER_SPEED
            if keys[pygame.K_d]:
                player_rect.x += PLAYER_SPEED

            player_rect.x = max(0, min(player_rect.x, SCREEN_WIDTH - PLAYER_SIZE))

            if jump_pressed and player_rect.bottom == GROUND_Y:
                player_y_velocity = JUMP_STRENGTH

            player_y_velocity += GRAVITY
            player_rect.y += player_y_velocity

            if player_rect.bottom >= GROUND_Y:
                player_rect.bottom = GROUND_Y
                player_y_velocity = 0

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

        if game_state == "paused":
            pause_buttons = draw_pause_menu(screen, title_font, font, selected_pause_option)
        elif game_state == "controls":
            controls_back_button = draw_controls_menu(screen, title_font, font, small_font)

        pygame.display.flip()
        clock.tick(FPS)

        frames_run += 1
        if max_frames is not None and frames_run >= max_frames:
            running = False

    pygame.quit()


if __name__ == "__main__":
    run_game()
