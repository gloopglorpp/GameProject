import math

import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
PLAYER_SCREEN_X = 160

PLAYER_SIZE = 50
PLAYER_SPEED = 5
JUMP_STRENGTH = -16
GRAVITY = 1
PLAYER_COLOR = (25, 31, 29)
PLAYER_LINE_WIDTH = 5
PLAYER_HEAD_RADIUS = 8
WALK_ANIMATION_SPEED = 0.28
ROBE_COLOR = (37, 67, 130)
ROBE_SHADOW_COLOR = (24, 39, 86)
HAT_COLOR = (41, 91, 172)
HAT_TRIM_COLOR = (128, 185, 238)
SPARKLE_COLOR = (210, 235, 255)
STAFF_COLOR = (96, 62, 35)
STAFF_GLOW_COLOR = (255, 190, 92)

FIREBALL_SPEED = 9
FIREBALL_RADIUS = 8
FIREBALL_LIFETIME = 90
FIREBALL_CORE_COLOR = (255, 230, 120)
FIREBALL_MID_COLOR = (255, 118, 31)
FIREBALL_EDGE_COLOR = (185, 38, 13)
FIREBALL_GLOW_COLOR = (255, 126, 28, 95)

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
CLOUD_COLOR = (224, 229, 222, 90)
GRASS_HIGHLIGHT_COLOR = (112, 148, 87)
TEXT_COLOR = (235, 238, 245)
MUTED_TEXT_COLOR = (155, 165, 180)
MENU_OVERLAY_COLOR = (12, 16, 18, 175)
MENU_PANEL_COLOR = (34, 42, 43)
MENU_SELECTED_COLOR = (92, 121, 105)
PAUSE_OPTIONS = ["Resume", "Controls", "Quit"]


def draw_text(screen, font, text, x, y, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_mountains(screen, points, color, offset_x):
    mountain_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(mountain_layer, color, points)
    pygame.draw.polygon(mountain_layer, color, [(x + SCREEN_WIDTH, y) for x, y in points])
    screen.blit(mountain_layer, (-offset_x, 0))


def draw_clouds(screen, world_x, background_time):
    cloud_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    cloud_positions = [
        (120, 95, 58, 15, 0.08),
        (360, 130, 78, 18, 0.12),
        (620, 80, 64, 14, 0.1),
    ]

    for base_x, y, width, height, speed in cloud_positions:
        x = (base_x - world_x * speed - background_time * speed * 0.4) % (SCREEN_WIDTH + width) - width
        pygame.draw.ellipse(cloud_layer, CLOUD_COLOR, (x, y, width, height))
        pygame.draw.ellipse(cloud_layer, CLOUD_COLOR, (x + width * 0.3, y - 8, width * 0.5, height * 1.4))

    screen.blit(cloud_layer, (0, 0))


def draw_grass_highlights(screen, world_x, background_time):
    for index in range(18):
        x = (index * 55 - world_x * 0.9) % (SCREEN_WIDTH + 60) - 30
        height = 7 + (index + background_time // 15) % 4
        pygame.draw.line(
            screen,
            GRASS_HIGHLIGHT_COLOR,
            (x, GROUND_Y + 17),
            (x + 9, GROUND_Y + 17 - height),
            2,
        )


def draw_background(screen, world_x, background_time):
    screen.fill(SKY_COLOR)
    draw_clouds(screen, world_x, background_time)

    far_offset = int(world_x * 0.15) % SCREEN_WIDTH
    near_offset = int(world_x * 0.35) % SCREEN_WIDTH

    far_mountains = [
        (0, GROUND_Y),
        (0, 250),
        (120, 170),
        (260, 285),
        (390, 155),
        (570, 305),
        (700, 205),
        (SCREEN_WIDTH, 270),
        (SCREEN_WIDTH, GROUND_Y),
    ]

    near_mountains = [
        (0, GROUND_Y),
        (0, 335),
        (110, 260),
        (210, 345),
        (340, 235),
        (475, 355),
        (615, 245),
        (SCREEN_WIDTH, 350),
        (SCREEN_WIDTH, GROUND_Y),
    ]

    draw_mountains(screen, far_mountains, MOUNTAIN_FAR_COLOR, far_offset)
    draw_mountains(screen, near_mountains, MOUNTAIN_NEAR_COLOR, near_offset)

    pygame.draw.rect(screen, GRASS_COLOR, (0, GROUND_Y, SCREEN_WIDTH, 18))
    draw_grass_highlights(screen, world_x, background_time)
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
        "Space: jump",
        "Left click: cast fireball",
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


def get_staff_points(player_rect, player_facing, front_hand):
    staff_top = (front_hand[0] + player_facing * 11, front_hand[1] - 24)
    staff_bottom = (front_hand[0] - player_facing * 7, front_hand[1] + 17)
    return staff_top, staff_bottom


def draw_player(screen, player_rect, player_facing, animation_frame, is_moving, is_jumping, background_time):
    step = math.sin(animation_frame) if is_moving else 0
    bounce = abs(step) * 2 if is_moving and not is_jumping else 0

    head_center = (player_rect.centerx, player_rect.y + 9 - bounce)
    neck = (player_rect.centerx, player_rect.y + 19 - bounce)
    hip = (player_rect.centerx, player_rect.y + 34 - bounce)

    if is_jumping:
        front_hand = (player_rect.centerx + player_facing * 18, player_rect.y + 24)
        back_hand = (player_rect.centerx - player_facing * 15, player_rect.y + 24)
        front_foot = (player_rect.centerx + player_facing * 11, player_rect.bottom - 6)
        back_foot = (player_rect.centerx - player_facing * 13, player_rect.bottom - 9)
    else:
        arm_swing = step * 8
        leg_swing = step * 13
        front_hand = (player_rect.centerx + player_facing * (18 - arm_swing), player_rect.y + 27 - bounce)
        back_hand = (player_rect.centerx - player_facing * (13 - arm_swing), player_rect.y + 28 - bounce)
        front_foot = (player_rect.centerx + player_facing * (15 + leg_swing), player_rect.bottom)
        back_foot = (player_rect.centerx - player_facing * (13 + leg_swing), player_rect.bottom)

    robe_points = [
        (player_rect.centerx - 13, player_rect.y + 20 - bounce),
        (player_rect.centerx + 13, player_rect.y + 20 - bounce),
        (player_rect.centerx + 19, player_rect.bottom),
        (player_rect.centerx - 19, player_rect.bottom),
    ]
    hat_points = [
        (player_rect.centerx - 15, player_rect.y + 4 - bounce),
        (player_rect.centerx + 15, player_rect.y + 4 - bounce),
        (player_rect.centerx + player_facing * 5, player_rect.y - 25 - bounce),
    ]
    staff_top, staff_bottom = get_staff_points(player_rect, player_facing, front_hand)

    pygame.draw.line(screen, PLAYER_COLOR, hip, front_foot, PLAYER_LINE_WIDTH)
    pygame.draw.line(screen, PLAYER_COLOR, hip, back_foot, PLAYER_LINE_WIDTH)
    pygame.draw.polygon(screen, ROBE_COLOR, robe_points)
    pygame.draw.line(screen, ROBE_SHADOW_COLOR, robe_points[0], robe_points[3], 3)
    pygame.draw.circle(screen, PLAYER_COLOR, head_center, PLAYER_HEAD_RADIUS)
    pygame.draw.polygon(screen, HAT_COLOR, hat_points)
    pygame.draw.line(screen, HAT_TRIM_COLOR, hat_points[0], hat_points[1], 3)
    pygame.draw.line(screen, PLAYER_COLOR, neck, front_hand, PLAYER_LINE_WIDTH)
    pygame.draw.line(screen, PLAYER_COLOR, neck, back_hand, PLAYER_LINE_WIDTH)
    pygame.draw.line(screen, STAFF_COLOR, staff_bottom, staff_top, 5)
    pygame.draw.circle(screen, STAFF_GLOW_COLOR, staff_top, 5)

    for offset in (0, 11, 23):
        sparkle_x = player_rect.centerx - 8 + (offset % 3) * 8
        sparkle_y = player_rect.y + 9 + ((background_time + offset) % 30) // 10 * 9
        pygame.draw.circle(screen, SPARKLE_COLOR, (sparkle_x, sparkle_y), 1)


def draw_fireball(screen, fireball, world_x):
    screen_x = int(fireball["x"] - world_x + PLAYER_SCREEN_X)
    y = int(fireball["y"])
    direction = fireball["direction"]

    glow = pygame.Surface((54, 38), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, FIREBALL_GLOW_COLOR, (0, 0, 54, 38))
    screen.blit(glow, (screen_x - 27, y - 19))

    for index in range(3):
        trail_x = screen_x - direction * (12 + index * 9)
        trail_radius = max(2, FIREBALL_RADIUS - index * 2)
        pygame.draw.circle(screen, FIREBALL_EDGE_COLOR, (trail_x, y), trail_radius)

    pygame.draw.circle(screen, FIREBALL_EDGE_COLOR, (screen_x, y), FIREBALL_RADIUS + 3)
    pygame.draw.circle(screen, FIREBALL_MID_COLOR, (screen_x, y), FIREBALL_RADIUS)
    pygame.draw.circle(screen, FIREBALL_CORE_COLOR, (screen_x - direction * 2, y - 2), FIREBALL_RADIUS // 2)


def get_fireball_rect(fireball, world_x):
    screen_x = int(fireball["x"] - world_x + PLAYER_SCREEN_X)
    return pygame.Rect(
        screen_x - FIREBALL_RADIUS,
        int(fireball["y"] - FIREBALL_RADIUS),
        FIREBALL_RADIUS * 2,
        FIREBALL_RADIUS * 2,
    )


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

    player_rect = pygame.Rect(PLAYER_SCREEN_X, GROUND_Y - PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE)
    enemy_world_x = 500
    enemy_rect = pygame.Rect(enemy_world_x, GROUND_Y - ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)

    enemy_max_health = 3
    enemy_health = enemy_max_health
    enemy_text = ""
    enemy_text_timer = 0
    player_y_velocity = 0
    player_facing = 1
    player_animation_frame = 0
    player_is_moving = False
    fireballs = []
    world_x = 0
    background_time = 0
    selected_pause_option = 0
    game_state = "playing"
    frames_run = 0
    running = True

    while running:
        cast_pressed = False
        jump_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION and game_state == "paused":
                for index, (_, rect) in enumerate(get_pause_buttons()):
                    if rect.collidepoint(event.pos):
                        selected_pause_option = index
            elif event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "paused"
                    elif event.key == pygame.K_SPACE:
                        jump_pressed = True
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
                    elif event.key == pygame.K_RETURN:
                        if selected_pause_option == 0:
                            game_state = "playing"
                        elif selected_pause_option == 1:
                            game_state = "controls"
                        else:
                            running = False
                elif game_state == "controls":
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                        game_state = "paused"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "playing":
                    cast_pressed = True
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
            background_time += 1
            enemy_rect.x = int(enemy_world_x - world_x + PLAYER_SCREEN_X)
            keys = pygame.key.get_pressed()
            player_is_moving = False

            if keys[pygame.K_a]:
                world_x = max(0, world_x - PLAYER_SPEED)
                player_facing = -1
                player_is_moving = True
            if keys[pygame.K_d]:
                world_x += PLAYER_SPEED
                player_facing = 1
                player_is_moving = True

            if player_is_moving:
                player_animation_frame += WALK_ANIMATION_SPEED
            else:
                player_animation_frame = 0

            player_rect.x = PLAYER_SCREEN_X

            if jump_pressed and player_rect.bottom == GROUND_Y:
                player_y_velocity = JUMP_STRENGTH

            player_y_velocity += GRAVITY
            player_rect.y += player_y_velocity

            if player_rect.bottom >= GROUND_Y:
                player_rect.bottom = GROUND_Y
                player_y_velocity = 0

            if cast_pressed:
                front_hand = (
                    player_rect.centerx + player_facing * 18,
                    player_rect.y + 24 if player_rect.bottom < GROUND_Y else player_rect.y + 27,
                )
                staff_top, _ = get_staff_points(player_rect, player_facing, front_hand)
                fireballs.append({
                    "x": world_x + staff_top[0] - PLAYER_SCREEN_X,
                    "y": staff_top[1],
                    "direction": player_facing,
                    "age": 0,
                })

            for fireball in fireballs[:]:
                fireball["x"] += FIREBALL_SPEED * fireball["direction"]
                fireball["age"] += 1
                fireball_rect = get_fireball_rect(fireball, world_x)

                if fireball_rect.colliderect(enemy_rect) and enemy_health > 0:
                    enemy_health = max(enemy_health - 1, 0)
                    fireballs.remove(fireball)

                    if enemy_health == 2:
                        enemy_text = "???"
                    elif enemy_health == 1:
                        enemy_text = "HOT!!"
                    else:
                        enemy_text = "Defeated!"

                    enemy_text_timer = 60
                elif fireball["age"] > FIREBALL_LIFETIME:
                    fireballs.remove(fireball)

            if enemy_text_timer > 0:
                enemy_text_timer -= 1

        enemy_rect.x = int(enemy_world_x - world_x + PLAYER_SCREEN_X)

        draw_background(screen, world_x, background_time)

        for fireball in fireballs:
            draw_fireball(screen, fireball, world_x)

        player_is_jumping = player_rect.bottom < GROUND_Y or player_y_velocity != 0
        draw_player(
            screen,
            player_rect,
            player_facing,
            player_animation_frame,
            player_is_moving,
            player_is_jumping,
            background_time,
        )
        if -ENEMY_SIZE <= enemy_rect.x <= SCREEN_WIDTH:
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
