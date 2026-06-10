import math
import random

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

GROUND_Y = 485

SKY_TOP_COLOR = (246, 177, 104)
SKY_MID_COLOR = (224, 133, 83)
SKY_BOTTOM_COLOR = (103, 91, 86)
SUN_GLOW_COLOR = (255, 213, 139, 45)
MIST_COLOR = (255, 222, 177, 42)
DISTANT_HILL_COLOR = (91, 79, 76, 82)
MID_HILL_COLOR = (69, 55, 50, 135)
SHACK_COLOR = (42, 33, 29, 155)
SHACK_WINDOW_COLOR = (246, 167, 82, 70)
TREE_FAR_COLOR = (42, 34, 31, 170)
TREE_NEAR_COLOR = (22, 19, 17, 230)
GRASS_COLOR = (63, 82, 55)
GROUND_COLOR = (32, 34, 29)
GROUND_SHADOW_COLOR = (18, 19, 18)
GRASS_HIGHLIGHT_COLOR = (125, 147, 87)
FIREFLY_COLOR = (255, 211, 121, 105)
VIGNETTE_COLOR = (21, 15, 14, 95)
TEXT_COLOR = (235, 238, 245)
MUTED_TEXT_COLOR = (155, 165, 180)
MENU_OVERLAY_COLOR = (12, 16, 18, 175)
MENU_PANEL_COLOR = (34, 42, 43)
MENU_SELECTED_COLOR = (92, 121, 105)
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
    for y in range(GROUND_Y):
        if y < GROUND_Y * 0.55:
            amount = y / (GROUND_Y * 0.55)
            color = blend_color(SKY_TOP_COLOR, SKY_MID_COLOR, amount)
        else:
            amount = (y - GROUND_Y * 0.55) / (GROUND_Y * 0.45)
            color = blend_color(SKY_MID_COLOR, SKY_BOTTOM_COLOR, amount)
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))


def draw_sun_glow(screen, background_time):
    glow = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pulse = math.sin(background_time * 0.012) * 5
    center = (SCREEN_WIDTH // 2 + 45, 260)

    for index, radius in enumerate((255, 205, 155, 105, 65)):
        alpha = max(8, SUN_GLOW_COLOR[3] - index * 7)
        pygame.draw.circle(glow, (*SUN_GLOW_COLOR[:3], alpha), center, int(radius + pulse))

    screen.blit(glow, (0, 0))


def parallax_x(base_x, world_x, speed, spacing):
    return (base_x - world_x * speed) % spacing - spacing * 0.22


def draw_hill_layer(screen, world_x, speed, color, base_y, wave_height, spacing):
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    points = [(0, GROUND_Y + 18)]

    for x in range(-80, SCREEN_WIDTH + 121, 80):
        wave = math.sin((x + world_x * speed) * 0.011) * wave_height
        y = base_y + wave
        points.append((x, int(y)))

    points.extend([(SCREEN_WIDTH, GROUND_Y + 18), (0, GROUND_Y + 18)])
    pygame.draw.polygon(layer, color, points)

    for base_x in (120, 420, 740, 1040):
        x = parallax_x(base_x, world_x, speed, spacing)
        pygame.draw.ellipse(layer, (*color[:3], max(15, color[3] - 28)), (x - 90, base_y - 12, 230, 64))

    screen.blit(layer, (0, 0))


def draw_mist(screen, world_x, background_time):
    mist = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for index in range(5):
        y = 265 + index * 34
        width = 290 + index * 65
        height = 44 + index * 8
        speed = 0.055 + index * 0.018
        x = (index * 180 - world_x * speed - background_time * 0.12) % (SCREEN_WIDTH + width) - width
        pygame.draw.ellipse(mist, MIST_COLOR, (x, y, width, height))
        pygame.draw.ellipse(mist, MIST_COLOR, (x + width * 0.72, y + 8, width * 0.7, height * 0.75))

    screen.blit(mist, (0, 0))


def draw_shack(screen, world_x):
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for base_x in (650, 1650):
        x = int(parallax_x(base_x, world_x, 0.24, 1250))
        y = GROUND_Y - 112
        wall = [(x, y + 40), (x + 118, y + 32), (x + 108, y + 100), (x + 8, y + 104)]
        roof = [(x - 10, y + 43), (x + 54, y - 2), (x + 130, y + 34), (x + 112, y + 45)]
        door = pygame.Rect(x + 68, y + 62, 26, 39)
        window = pygame.Rect(x + 24, y + 55, 22, 18)

        pygame.draw.polygon(layer, SHACK_COLOR, wall)
        pygame.draw.polygon(layer, (*SHACK_COLOR[:3], SHACK_COLOR[3] + 35), roof)
        pygame.draw.rect(layer, (*GROUND_SHADOW_COLOR, 190), door)
        pygame.draw.rect(layer, SHACK_WINDOW_COLOR, window, border_radius=2)

        for plank_x in (x + 10, x + 37, x + 64, x + 92):
            pygame.draw.line(layer, (*GROUND_SHADOW_COLOR, 100), (plank_x, y + 43), (plank_x - 4, y + 102), 2)

        pygame.draw.line(layer, (*GROUND_SHADOW_COLOR, 150), (x + 7, y + 104), (x - 7, GROUND_Y + 6), 4)
        pygame.draw.line(layer, (*GROUND_SHADOW_COLOR, 150), (x + 112, y + 98), (x + 128, GROUND_Y + 5), 4)

    screen.blit(layer, (0, 0))


def draw_big_tree(screen, world_x, background_time):
    layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for base_x, scale, color, speed in ((260, 1.08, TREE_FAR_COLOR, 0.18), (1180, 1.22, TREE_NEAR_COLOR, 0.34)):
        x = int(parallax_x(base_x, world_x, speed, 1350))
        root_y = GROUND_Y + 18
        trunk = [
            (x - int(34 * scale), root_y),
            (x - int(19 * scale), int(210 * scale) - 28),
            (x + int(16 * scale), int(186 * scale) - 28),
            (x + int(43 * scale), root_y),
        ]
        pygame.draw.polygon(layer, color, trunk)

        branches = [
            ((x + int(2 * scale), 205), (x - int(128 * scale), 166), 15),
            ((x + int(4 * scale), 196), (x + int(150 * scale), 130), 17),
            ((x + int(12 * scale), 228), (x + int(120 * scale), 214), 11),
            ((x - int(5 * scale), 246), (x - int(98 * scale), 250), 10),
        ]

        for start_point, end_point, width in branches:
            pygame.draw.line(layer, color, start_point, end_point, max(2, int(width * scale)))
            twig_end = (end_point[0] + int(34 * scale), end_point[1] - int(29 * scale))
            pygame.draw.line(layer, color, end_point, twig_end, max(2, int(width * scale * 0.35)))
            twig_end = (end_point[0] - int(28 * scale), end_point[1] + int(22 * scale))
            pygame.draw.line(layer, color, end_point, twig_end, max(2, int(width * scale * 0.3)))

        rope_top = (x - int(113 * scale), 170)
        sway = math.sin(background_time * 0.035 + base_x) * 9
        rope_bottom = (int(rope_top[0] + sway), int(312 * scale) - 8)
        seat_left = (rope_bottom[0] - int(23 * scale), rope_bottom[1] + int(32 * scale))
        seat_right = (rope_bottom[0] + int(23 * scale), rope_bottom[1] + int(32 * scale))
        pygame.draw.line(layer, (*color[:3], min(255, color[3] + 25)), rope_top, rope_bottom, max(2, int(2 * scale)))
        pygame.draw.line(layer, (*color[:3], min(255, color[3] + 25)), rope_bottom, seat_left, max(1, int(2 * scale)))
        pygame.draw.line(layer, (*color[:3], min(255, color[3] + 25)), rope_bottom, seat_right, max(1, int(2 * scale)))
        pygame.draw.line(layer, (*color[:3], min(255, color[3] + 35)), seat_left, seat_right, max(3, int(5 * scale)))

    screen.blit(layer, (0, 0))


def draw_fireflies(screen, world_x, background_time):
    firefly_layer = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    for index in range(22):
        drift = math.sin(background_time * 0.025 + index * 1.7)
        x = (index * 73 - world_x * 0.12 + drift * 9) % (SCREEN_WIDTH + 60) - 30
        y = 235 + (index * 37) % 180 + math.sin(background_time * 0.018 + index) * 6
        radius = 1 + index % 2
        pygame.draw.circle(firefly_layer, FIREFLY_COLOR, (int(x), int(y)), radius)

    screen.blit(firefly_layer, (0, 0))


def draw_foreground_ground(screen, world_x, background_time):
    ground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    ridge = [(0, GROUND_Y)]

    for x in range(-20, SCREEN_WIDTH + 40, 40):
        y = GROUND_Y + math.sin((x + world_x * 0.28) * 0.018) * 7
        ridge.append((x, int(y)))

    ridge.extend([(SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)])
    pygame.draw.polygon(ground, (*GRASS_COLOR, 235), ridge)
    pygame.draw.rect(ground, (*GROUND_COLOR, 245), (0, GROUND_Y + 28, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))
    pygame.draw.rect(ground, (*GROUND_SHADOW_COLOR, 245), (0, GROUND_Y + 72, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))

    for index in range(34):
        x = int((index * 31 - world_x * 0.95) % (SCREEN_WIDTH + 70) - 35)
        height = 8 + (index % 5) * 3 + math.sin(background_time * 0.05 + index) * 2
        color = GRASS_HIGHLIGHT_COLOR if index % 3 else TREE_NEAR_COLOR[:3]
        pygame.draw.line(ground, (*color, 180), (x, GROUND_Y + 8), (x + 7, int(GROUND_Y + 8 - height)), 2)

    screen.blit(ground, (0, 0))


def draw_vignette(screen):
    vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(vignette, VIGNETTE_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), width=26)
    pygame.draw.rect(vignette, (*VIGNETTE_COLOR[:3], 45), (26, 26, SCREEN_WIDTH - 52, SCREEN_HEIGHT - 52), width=18)
    screen.blit(vignette, (0, 0))


def draw_background(screen, world_x, background_time):
    draw_sky_gradient(screen)
    draw_sun_glow(screen, background_time)
    draw_hill_layer(screen, world_x, 0.08, DISTANT_HILL_COLOR, 330, 18, 1050)
    draw_mist(screen, world_x, background_time)
    draw_hill_layer(screen, world_x, 0.16, MID_HILL_COLOR, 382, 22, 1120)
    draw_shack(screen, world_x)
    draw_big_tree(screen, world_x, background_time)
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
        "A / D: move",
        "Space: jump",
        "Left click: cast fireball",
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
            update_death_particles(death_particles)

            if enemy_health == 0:
                enemy_respawn_timer -= 1
                if enemy_respawn_timer <= 0 and not death_particles:
                    enemy_health = enemy_max_health
                    enemy_world_x = respawn_enemy(world_x)

            if enemy_health > 0:
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

                    if enemy_health == 0:
                        death_particles.extend(create_enemy_death_effect(enemy_rect, world_x))
                        enemy_respawn_timer = ENEMY_DEATH_RESPAWN_DELAY
                elif fireball["age"] > FIREBALL_LIFETIME:
                    fireballs.remove(fireball)

        enemy_rect.x = int(enemy_world_x - world_x + PLAYER_SCREEN_X)

        draw_background(screen, world_x, background_time)

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
        if enemy_health > 0 and -ENEMY_SIZE <= enemy_rect.x <= SCREEN_WIDTH:
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
