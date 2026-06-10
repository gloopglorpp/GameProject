import math
import random

import pygame


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
PLAYER_SCREEN_X = 280

PLAYER_SIZE = 56
PLAYER_SPEED = 3
JUMP_STRENGTH = -16
GRAVITY = 1
PLAYER_COLOR = (13, 14, 14)
PLAYER_LINE_WIDTH = 5
PLAYER_HEAD_RADIUS = 8
WALK_ANIMATION_SPEED = 0.16
ROBE_COLOR = (20, 21, 20)
ROBE_SHADOW_COLOR = (6, 7, 7)
HAT_COLOR = (30, 24, 22)
HAT_TRIM_COLOR = (122, 69, 45)
SPARKLE_COLOR = (255, 184, 91)
STAFF_COLOR = (96, 62, 35)
STAFF_GLOW_COLOR = (255, 158, 70)

FIREBALL_SPEED = 9
FIREBALL_RADIUS = 8
FIREBALL_LIFETIME = 90
FIREBALL_CORE_COLOR = (255, 230, 120)
FIREBALL_MID_COLOR = (255, 118, 31)
FIREBALL_EDGE_COLOR = (185, 38, 13)
FIREBALL_GLOW_COLOR = (255, 126, 28, 95)

ENEMY_SIZE = 50
ENEMY_SPEED = 0.55
ZOMBIE_SKIN_COLOR = (93, 128, 91)
ZOMBIE_SHADOW_COLOR = (54, 78, 56)
ZOMBIE_CLOTH_COLOR = (62, 71, 74)
ZOMBIE_EYE_COLOR = (214, 230, 196)
ENEMY_DEATH_RESPAWN_DELAY = 150
ENEMY_RESPAWN_DISTANCE_MIN = 860
ENEMY_RESPAWN_DISTANCE_MAX = 1180
FLAME_COLORS = [
    (255, 231, 132),
    (255, 155, 48),
    (222, 68, 24),
    (135, 36, 23),
]
SMOKE_COLORS = [
    (42, 43, 40),
    (78, 80, 76),
    (120, 122, 116),
]

GROUND_Y = 610

SKY_TOP_COLOR = (64, 42, 54)
SKY_MID_COLOR = (182, 82, 58)
SKY_BOTTOM_COLOR = (255, 175, 76)
SUN_GLOW_COLOR = (255, 194, 85, 58)
MIST_COLOR = (255, 211, 154, 34)
DISTANT_TREE_COLOR = (75, 52, 55, 62)
MID_TREE_COLOR = (46, 35, 36, 118)
DISTANT_HILL_COLOR = (85, 64, 60, 88)
MID_HILL_COLOR = (48, 38, 35, 155)
SHACK_COLOR = (20, 17, 16, 225)
SHACK_DETAIL_COLOR = (91, 60, 42, 130)
SHACK_WINDOW_COLOR = (255, 177, 82, 92)
TREE_FAR_COLOR = (31, 25, 23, 190)
TREE_NEAR_COLOR = (9, 9, 8, 248)
CANOPY_COLOR = (12, 10, 10, 225)
GRASS_COLOR = (33, 39, 30)
GROUND_COLOR = (18, 19, 17)
GROUND_SHADOW_COLOR = (8, 9, 8)
GRASS_HIGHLIGHT_COLOR = (105, 111, 68)
FIREFLY_COLOR = (255, 211, 121, 118)
VIGNETTE_COLOR = (11, 8, 10, 122)
TEXT_COLOR = (235, 238, 245)
MUTED_TEXT_COLOR = (155, 165, 180)
MENU_OVERLAY_COLOR = (12, 16, 18, 175)
MENU_PANEL_COLOR = (34, 42, 43)
MENU_SELECTED_COLOR = (92, 121, 105)
OPENING_SCENE_MODE = True
PAUSE_OPTIONS = ["Resume", "Controls", "Quit"]


def draw_text(screen, font, text, x, y, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def blend_color(start_color, end_color, amount):
    return tuple(
        int(start + (end - start) * amount)
        for start, end in zip(start_color, end_color)
    )


def draw_sky_gradient(screen):
    for y in range(SCREEN_HEIGHT):
        if y < SCREEN_HEIGHT * 0.48:
            amount = y / (SCREEN_HEIGHT * 0.48)
            color = blend_color(SKY_TOP_COLOR, SKY_MID_COLOR, amount)
        else:
            amount = (y - SCREEN_HEIGHT * 0.48) / (SCREEN_HEIGHT * 0.52)
            color = blend_color(SKY_MID_COLOR, SKY_BOTTOM_COLOR, amount)
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))


def draw_sun_glow(screen, background_time):
    glow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pulse = math.sin(background_time * 0.01) * 7
    center = (SCREEN_WIDTH // 2 + 35, int(GROUND_Y * 0.54))

    for index, radius in enumerate((430, 340, 250, 168, 92)):
        alpha = max(7, SUN_GLOW_COLOR[3] - index * 8)
        pygame.draw.circle(glow, (*SUN_GLOW_COLOR[:3], alpha), center, int(radius + pulse))

    screen.blit(glow, (0, 0))


def parallax_x(base_x, world_x, speed, spacing):
    return (base_x - world_x * speed) % spacing - spacing * 0.08


def draw_distant_tree_layer(screen, world_x):
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for index in range(18):
        x = int((index * 165 - world_x * 0.055) % (SCREEN_WIDTH + 210) - 105)
        trunk_width = 12 + index % 5 * 5
        top = 88 + index % 6 * 24
        base = GROUND_Y - 38 + index % 4 * 9
        lean = (index % 3 - 1) * 13
        color = DISTANT_TREE_COLOR if index % 2 else MID_TREE_COLOR
        pygame.draw.polygon(
            layer,
            color,
            [
                (x - trunk_width, base),
                (x + lean - trunk_width // 2, top),
                (x + lean + trunk_width // 2, top),
                (x + trunk_width, base),
            ],
        )

        for branch in range(3):
            branch_y = top + 55 + branch * 60 + index % 4 * 7
            branch_length = 52 + branch * 18
            direction = -1 if (index + branch) % 2 else 1
            start = (x + lean // 2, branch_y)
            end = (x + direction * branch_length, branch_y - 32 + branch * 8)
            pygame.draw.line(layer, color, start, end, 3)

    screen.blit(layer, (0, 0))


def draw_hill_layer(screen, world_x, speed, color, base_y, wave_height, spacing):
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    points = [(0, GROUND_Y + 18)]

    for x in range(-120, SCREEN_WIDTH + 161, 80):
        wave = math.sin((x + world_x * speed) * 0.009) * wave_height
        y = base_y + wave
        points.append((x, int(y)))

    points.extend([(SCREEN_WIDTH, GROUND_Y + 18), (0, GROUND_Y + 18)])
    pygame.draw.polygon(layer, color, points)

    for base_x in (120, 390, 710, 1030, 1360):
        x = parallax_x(base_x, world_x, speed, spacing)
        pygame.draw.ellipse(layer, (*color[:3], max(14, color[3] - 30)), (x - 120, base_y - 18, 290, 82))

    screen.blit(layer, (0, 0))


def draw_mist(screen, world_x, background_time):
    mist = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for index in range(7):
        y = 300 + index * 34
        width = 450 + index * 72
        height = 56 + index * 7
        speed = 0.045 + index * 0.012
        x = (index * 230 - world_x * speed - background_time * 0.09) % (SCREEN_WIDTH + width) - width
        pygame.draw.ellipse(mist, MIST_COLOR, (x, y, width, height))
        pygame.draw.ellipse(mist, MIST_COLOR, (x + width * 0.58, y + 5, width * 0.78, height * 0.72))

    screen.blit(mist, (0, 0))


def draw_leaf_canopy(screen, world_x, background_time):
    canopy = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for index in range(92):
        drift = math.sin(background_time * 0.008 + index) * 3
        x = (index * 83 - world_x * 0.18 + drift) % (SCREEN_WIDTH + 180) - 90
        y = 8 + index * 37 % 155
        width = 58 + index % 6 * 18
        height = 24 + index % 5 * 9
        alpha = 42 + index % 5 * 26
        pygame.draw.ellipse(canopy, (*CANOPY_COLOR[:3], alpha), (x, y, width, height))

    pygame.draw.rect(canopy, (*CANOPY_COLOR[:3], 90), (0, 0, SCREEN_WIDTH, 32))
    screen.blit(canopy, (0, 0))


def draw_shack(screen, world_x):
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for base_x in (170, 2140):
        x = int(parallax_x(base_x, world_x, 0.27, 2200))
        y = GROUND_Y - 198
        wall = [(x, y + 72), (x + 220, y + 56), (x + 210, y + 184), (x + 10, y + 190)]
        roof = [(x - 28, y + 72), (x + 96, y + 10), (x + 244, y + 56), (x + 218, y + 82)]
        doorway = [(x + 145, y + 103), (x + 185, y + 100), (x + 184, y + 184), (x + 144, y + 187)]
        window = pygame.Rect(x + 54, y + 104, 38, 34)

        pygame.draw.polygon(layer, SHACK_COLOR, wall)
        pygame.draw.polygon(layer, (*SHACK_COLOR[:3], 245), roof)
        pygame.draw.polygon(layer, (*GROUND_SHADOW_COLOR, 240), doorway)
        pygame.draw.rect(layer, SHACK_WINDOW_COLOR, window, border_radius=2)
        pygame.draw.line(layer, (*GROUND_SHADOW_COLOR, 170), window.midtop, window.midbottom, 2)
        pygame.draw.line(layer, (*GROUND_SHADOW_COLOR, 170), window.midleft, window.midright, 2)

        for plank_x in (x + 22, x + 58, x + 94, x + 132, x + 174, x + 205):
            pygame.draw.line(layer, (*SHACK_DETAIL_COLOR[:3], 145), (plank_x, y + 75), (plank_x - 9, y + 188), 3)

        for board in range(7):
            board_x = x - 18 + board * 40
            board_y = GROUND_Y - 62 + math.sin(board) * 6
            pygame.draw.line(layer, (*SHACK_COLOR[:3], 200), (board_x, board_y), (board_x, GROUND_Y + 4), 5)
            pygame.draw.line(layer, (*SHACK_COLOR[:3], 180), (board_x - 20, board_y + 18), (board_x + 28, board_y + 10), 4)

        pygame.draw.line(layer, (*GROUND_SHADOW_COLOR, 190), (x + 10, y + 190), (x - 12, GROUND_Y + 9), 6)
        pygame.draw.line(layer, (*GROUND_SHADOW_COLOR, 190), (x + 212, y + 184), (x + 238, GROUND_Y + 7), 6)

    screen.blit(layer, (0, 0))


def draw_huge_tree(screen, world_x, background_time):
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    x = int(parallax_x(780, world_x, 0.34, 2100))
    root_y = GROUND_Y + 42
    trunk = [
        (x - 96, root_y),
        (x - 76, 388),
        (x - 64, 170),
        (x - 28, -30),
        (x + 86, -35),
        (x + 118, 188),
        (x + 100, 420),
        (x + 150, root_y),
    ]
    pygame.draw.polygon(layer, TREE_NEAR_COLOR, trunk)

    root_points = [
        [(x - 86, GROUND_Y), (x - 205, GROUND_Y + 25), (x - 40, GROUND_Y + 30)],
        [(x + 78, GROUND_Y), (x + 210, GROUND_Y + 16), (x + 38, GROUND_Y + 35)],
        [(x + 8, GROUND_Y - 2), (x - 15, GROUND_Y + 42), (x + 86, GROUND_Y + 42)],
    ]
    for points in root_points:
        pygame.draw.polygon(layer, TREE_NEAR_COLOR, points)

    main_branches = [
        ((x + 22, 142), (x - 360, 104), 42),
        ((x + 28, 165), (x + 370, 78), 46),
        ((x - 20, 225), (x - 280, 236), 26),
        ((x + 62, 236), (x + 310, 250), 30),
    ]
    for start_point, end_point, width in main_branches:
        pygame.draw.line(layer, TREE_NEAR_COLOR, start_point, end_point, width)
        twig_a = (end_point[0] - 55, end_point[1] - 42)
        twig_b = (end_point[0] + 68, end_point[1] + 28)
        pygame.draw.line(layer, TREE_NEAR_COLOR, end_point, twig_a, max(5, width // 4))
        pygame.draw.line(layer, TREE_NEAR_COLOR, end_point, twig_b, max(5, width // 5))

    rope_anchor_x = x + 315
    rope_top = (rope_anchor_x, 92)
    sway = math.sin(background_time * 0.028) * 12
    left_rope_bottom = (int(rope_anchor_x - 18 + sway), 374)
    right_rope_bottom = (int(rope_anchor_x + 18 + sway), 374)
    seat_left = (left_rope_bottom[0] - 25, left_rope_bottom[1] + 12)
    seat_right = (right_rope_bottom[0] + 25, right_rope_bottom[1] + 12)
    rope_color = (24, 20, 17, 245)
    pygame.draw.line(layer, rope_color, rope_top, left_rope_bottom, 3)
    pygame.draw.line(layer, rope_color, (rope_top[0] + 36, rope_top[1] - 3), right_rope_bottom, 3)
    pygame.draw.line(layer, rope_color, seat_left, seat_right, 7)

    screen.blit(layer, (0, 0))


def draw_fireflies(screen, world_x, background_time):
    firefly_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for index in range(36):
        drift = math.sin(background_time * 0.022 + index * 1.7)
        x = (index * 89 - world_x * 0.1 + drift * 10) % (SCREEN_WIDTH + 80) - 40
        y = 275 + (index * 47) % 250 + math.sin(background_time * 0.017 + index) * 8
        radius = 1 + index % 2
        pygame.draw.circle(firefly_layer, FIREFLY_COLOR, (int(x), int(y)), radius)

    screen.blit(firefly_layer, (0, 0))


def draw_foreground_ground(screen, world_x, background_time):
    ground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    ridge = [(0, GROUND_Y)]

    for x in range(-40, SCREEN_WIDTH + 60, 36):
        y = GROUND_Y + math.sin((x + world_x * 0.22) * 0.016) * 8
        ridge.append((x, int(y)))

    ridge.extend([(SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
    pygame.draw.polygon(ground, (*GRASS_COLOR, 244), ridge)
    pygame.draw.rect(ground, (*GROUND_COLOR, 248), (0, GROUND_Y + 26, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
    pygame.draw.rect(ground, (*GROUND_SHADOW_COLOR, 250), (0, GROUND_Y + 80, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))

    for index in range(76):
        x = int((index * 28 - world_x * 0.72) % (SCREEN_WIDTH + 90) - 45)
        height = 10 + (index % 7) * 4 + math.sin(background_time * 0.038 + index) * 3
        lean = -7 + index % 15
        color = GRASS_HIGHLIGHT_COLOR if index % 4 else TREE_NEAR_COLOR[:3]
        pygame.draw.line(ground, (*color, 188), (x, GROUND_Y + 10), (x + lean, int(GROUND_Y + 10 - height)), 2)

    screen.blit(ground, (0, 0))


def draw_vignette(screen):
    vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(vignette, VIGNETTE_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), width=38)
    pygame.draw.rect(vignette, (*VIGNETTE_COLOR[:3], 58), (38, 38, SCREEN_WIDTH - 76, SCREEN_HEIGHT - 76), width=22)
    screen.blit(vignette, (0, 0))


def draw_background(screen, world_x, background_time):
    draw_sky_gradient(screen)
    draw_sun_glow(screen, background_time)
    draw_distant_tree_layer(screen, world_x)
    draw_hill_layer(screen, world_x, 0.07, DISTANT_HILL_COLOR, 430, 24, 1500)
    draw_mist(screen, world_x, background_time)
    draw_hill_layer(screen, world_x, 0.15, MID_HILL_COLOR, 510, 24, 1620)
    draw_shack(screen, world_x)
    draw_huge_tree(screen, world_x, background_time)
    draw_leaf_canopy(screen, world_x, background_time)
    draw_fireflies(screen, world_x, background_time)
    draw_foreground_ground(screen, world_x, background_time)
    draw_vignette(screen)


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
        "A / D: slow walk",
        "Space: jump",
        "Esc: pause or return",
    ]

    if not OPENING_SCENE_MODE:
        controls.insert(2, "Left click: cast fireball")

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
    bounce = abs(step) * 1.5 if is_moving and not is_jumping else 0

    shadow = pygame.Surface((82, 26), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 90), (0, 0, 82, 20))
    screen.blit(shadow, (player_rect.centerx - 41, GROUND_Y - 8))

    head_center = (player_rect.centerx, player_rect.y + 12 - bounce)
    neck = (player_rect.centerx, player_rect.y + 24 - bounce)
    hip = (player_rect.centerx, player_rect.y + 39 - bounce)

    if is_jumping:
        front_hand = (player_rect.centerx + player_facing * 18, player_rect.y + 28)
        back_hand = (player_rect.centerx - player_facing * 13, player_rect.y + 30)
        front_foot = (player_rect.centerx + player_facing * 10, player_rect.bottom - 7)
        back_foot = (player_rect.centerx - player_facing * 12, player_rect.bottom - 10)
    else:
        arm_swing = step * 5
        leg_swing = step * 9
        front_hand = (player_rect.centerx + player_facing * (18 - arm_swing), player_rect.y + 31 - bounce)
        back_hand = (player_rect.centerx - player_facing * (12 - arm_swing), player_rect.y + 32 - bounce)
        front_foot = (player_rect.centerx + player_facing * (11 + leg_swing), player_rect.bottom)
        back_foot = (player_rect.centerx - player_facing * (10 + leg_swing), player_rect.bottom)

    cloak_points = [
        (player_rect.centerx - 16, player_rect.y + 22 - bounce),
        (player_rect.centerx + 15, player_rect.y + 22 - bounce),
        (player_rect.centerx + 22, player_rect.bottom - 4),
        (player_rect.centerx + 8, player_rect.bottom),
        (player_rect.centerx - 4, player_rect.bottom - 5),
        (player_rect.centerx - 21, player_rect.bottom),
    ]
    hood_points = [
        (player_rect.centerx - 13, player_rect.y + 9 - bounce),
        (player_rect.centerx + 13, player_rect.y + 8 - bounce),
        (player_rect.centerx + player_facing * 8, player_rect.y - 8 - bounce),
    ]

    pygame.draw.line(screen, ROBE_SHADOW_COLOR, hip, front_foot, PLAYER_LINE_WIDTH)
    pygame.draw.line(screen, ROBE_SHADOW_COLOR, hip, back_foot, PLAYER_LINE_WIDTH)
    pygame.draw.polygon(screen, ROBE_COLOR, cloak_points)
    pygame.draw.line(screen, HAT_TRIM_COLOR, cloak_points[0], cloak_points[3], 2)
    pygame.draw.circle(screen, PLAYER_COLOR, head_center, PLAYER_HEAD_RADIUS + 2)
    pygame.draw.polygon(screen, HAT_COLOR, hood_points)
    pygame.draw.line(screen, PLAYER_COLOR, neck, front_hand, PLAYER_LINE_WIDTH)
    pygame.draw.line(screen, PLAYER_COLOR, neck, back_hand, PLAYER_LINE_WIDTH)

    lantern_center = (front_hand[0] + player_facing * 5, front_hand[1] + 8)
    lantern_glow = pygame.Surface((54, 54), pygame.SRCALPHA)
    glow_alpha = 45 + int((math.sin(background_time * 0.08) + 1) * 18)
    pygame.draw.circle(lantern_glow, (*STAFF_GLOW_COLOR, glow_alpha), (27, 27), 26)
    screen.blit(lantern_glow, (lantern_center[0] - 27, lantern_center[1] - 27))
    pygame.draw.line(screen, STAFF_COLOR, front_hand, lantern_center, 2)
    pygame.draw.rect(screen, PLAYER_COLOR, (lantern_center[0] - 5, lantern_center[1] - 4, 10, 12), border_radius=2)
    pygame.draw.circle(screen, SPARKLE_COLOR, lantern_center, 3)

    eye_x = head_center[0] + player_facing * 4
    pygame.draw.circle(screen, (240, 170, 92), (eye_x, head_center[1] - 1), 1)


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


def draw_zombie(screen, enemy_rect, enemy_health, enemy_max_health, background_time):
    if enemy_health > 0:
        step = math.sin(background_time * 0.09)
        head_center = (enemy_rect.centerx, enemy_rect.y + 11)
        body_rect = pygame.Rect(enemy_rect.x + 15, enemy_rect.y + 21, 22, 24)
        left_arm = (enemy_rect.x + 5, enemy_rect.y + 30 + step * 2)
        right_arm = (enemy_rect.right - 5, enemy_rect.y + 30 - step * 2)
        left_foot = (enemy_rect.centerx - 10 - step * 4, enemy_rect.bottom)
        right_foot = (enemy_rect.centerx + 9 + step * 4, enemy_rect.bottom)

        pygame.draw.line(screen, ZOMBIE_SHADOW_COLOR, (enemy_rect.centerx, enemy_rect.y + 34), left_foot, 5)
        pygame.draw.line(screen, ZOMBIE_SHADOW_COLOR, (enemy_rect.centerx, enemy_rect.y + 34), right_foot, 5)
        pygame.draw.rect(screen, ZOMBIE_CLOTH_COLOR, body_rect, border_radius=4)
        pygame.draw.line(screen, ZOMBIE_SKIN_COLOR, (enemy_rect.x + 16, enemy_rect.y + 25), left_arm, 5)
        pygame.draw.line(screen, ZOMBIE_SKIN_COLOR, (enemy_rect.right - 16, enemy_rect.y + 25), right_arm, 5)
        pygame.draw.circle(screen, ZOMBIE_SKIN_COLOR, head_center, 10)
        pygame.draw.circle(screen, ZOMBIE_SHADOW_COLOR, (head_center[0] - 4, head_center[1] + 2), 2)
        pygame.draw.circle(screen, ZOMBIE_EYE_COLOR, (head_center[0] + 4, head_center[1] - 2), 2)
        pygame.draw.line(screen, ZOMBIE_SHADOW_COLOR, (head_center[0] - 3, head_center[1] + 7), (head_center[0] + 6, head_center[1] + 5), 2)
    else:
        return

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


def create_enemy_death_effect(enemy_rect, world_x):
    effect_variants = ["pillar", "burst", "spiral"]
    variant = random.choice(effect_variants)
    particles = []
    origin_x = world_x + enemy_rect.centerx - PLAYER_SCREEN_X
    origin_y = enemy_rect.centery

    if variant == "pillar":
        flame_count = 24
        smoke_count = 20
        flame_spread = 12
    elif variant == "burst":
        flame_count = 34
        smoke_count = 14
        flame_spread = 26
    else:
        flame_count = 28
        smoke_count = 24
        flame_spread = 18

    for index in range(flame_count):
        angle = random.uniform(-math.pi * 0.95, -math.pi * 0.05)
        speed = random.uniform(1.4, 4.2)
        swirl = math.sin(index * 0.8) * 1.2 if variant == "spiral" else 0
        particles.append({
            "kind": "flame",
            "x": origin_x + random.uniform(-flame_spread, flame_spread),
            "y": origin_y + random.uniform(-18, 18),
            "vx": math.cos(angle) * speed + swirl,
            "vy": math.sin(angle) * speed - random.uniform(0.4, 1.5),
            "radius": random.uniform(4, 10),
            "age": 0,
            "life": random.randint(28, 52),
            "color": random.choice(FLAME_COLORS),
        })

    for _ in range(smoke_count):
        particles.append({
            "kind": "smoke",
            "x": origin_x + random.uniform(-18, 18),
            "y": origin_y + random.uniform(-18, 12),
            "vx": random.uniform(-0.65, 0.65),
            "vy": random.uniform(-1.5, -0.35),
            "radius": random.uniform(8, 17),
            "age": 0,
            "life": random.randint(70, 120),
            "color": random.choice(SMOKE_COLORS),
        })

    return particles


def update_death_particles(particles):
    for particle in particles[:]:
        particle["age"] += 1
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        if particle["kind"] == "flame":
            particle["vy"] -= 0.02
            particle["radius"] *= 0.965
        else:
            particle["vy"] -= 0.005
            particle["vx"] *= 0.99
            particle["radius"] *= 1.01

        if particle["age"] >= particle["life"] or particle["radius"] < 0.8:
            particles.remove(particle)


def draw_death_particles(screen, particles, world_x):
    for particle in particles:
        progress = particle["age"] / particle["life"]
        alpha = max(0, int(210 * (1 - progress)))
        if particle["kind"] == "smoke":
            alpha = max(0, int(125 * (1 - progress)))

        screen_x = int(particle["x"] - world_x + PLAYER_SCREEN_X)
        y = int(particle["y"])
        radius = max(1, int(particle["radius"]))
        surface = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*particle["color"], alpha), (radius + 2, radius + 2), radius)
        screen.blit(surface, (screen_x - radius - 2, y - radius - 2))


def respawn_enemy(world_x):
    return world_x + random.randint(ENEMY_RESPAWN_DISTANCE_MIN, ENEMY_RESPAWN_DISTANCE_MAX)


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
    enemy_respawn_timer = 0
    death_particles = []
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
                if game_state == "playing" and not OPENING_SCENE_MODE:
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
            if not OPENING_SCENE_MODE:
                update_death_particles(death_particles)

            if not OPENING_SCENE_MODE and enemy_health == 0:
                enemy_respawn_timer -= 1
                if enemy_respawn_timer <= 0 and not death_particles:
                    enemy_health = enemy_max_health
                    enemy_world_x = respawn_enemy(world_x)

            if not OPENING_SCENE_MODE and enemy_health > 0:
                if enemy_world_x > world_x + 42:
                    enemy_world_x -= ENEMY_SPEED
                elif enemy_world_x < world_x - 42:
                    enemy_world_x += ENEMY_SPEED
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

            if cast_pressed and not OPENING_SCENE_MODE:
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

            if OPENING_SCENE_MODE:
                fireballs.clear()

            for fireball in fireballs[:]:
                fireball["x"] += FIREBALL_SPEED * fireball["direction"]
                fireball["age"] += 1
                fireball_rect = get_fireball_rect(fireball, world_x)

                if fireball_rect.colliderect(enemy_rect) and enemy_health > 0:
                    enemy_health = max(enemy_health - 1, 0)
                    fireballs.remove(fireball)

                    if enemy_health == 0:
                        death_particles.extend(create_enemy_death_effect(enemy_rect, world_x))
                        enemy_respawn_timer = ENEMY_DEATH_RESPAWN_DELAY
                elif fireball["age"] > FIREBALL_LIFETIME:
                    fireballs.remove(fireball)

        enemy_rect.x = int(enemy_world_x - world_x + PLAYER_SCREEN_X)

        draw_background(screen, world_x, background_time)

        if not OPENING_SCENE_MODE:
            draw_death_particles(screen, death_particles, world_x)

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
        if not OPENING_SCENE_MODE and enemy_health > 0 and -ENEMY_SIZE <= enemy_rect.x <= SCREEN_WIDTH:
            draw_zombie(screen, enemy_rect, enemy_health, enemy_max_health, background_time)

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
