import math
import random
from pathlib import Path

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

BACKGROUND_DIR = Path(__file__).resolve().parent.parent / "assets" / "backgrounds"
BACKGROUND_LAYER_SPECS = [
    {"name": "sky", "filename": "sky.png", "speed": 0.0, "drift": 0.0, "tile": False},
    {"name": "far_trees", "filename": "far_trees.png", "speed": 0.08, "drift": 0.0, "tile": True},
    {"name": "fog", "filename": "fog.png", "speed": 0.04, "drift": 0.18, "tile": True},
    {"name": "mid_trees", "filename": "mid_trees.png", "speed": 0.18, "drift": 0.0, "tile": True},
    {"name": "shack", "filename": "shack.png", "speed": 0.28, "drift": 0.0, "tile": True, "width_ratio": 0.42, "align": "bottom", "spacing": 1900},
    {"name": "foreground", "filename": "foreground.png", "speed": 0.55, "drift": 0.0, "tile": True},
]
BACKGROUND_PLACEHOLDER_COLORS = {
    "sky": (178, 90, 62, 255),
    "far_trees": (65, 45, 52, 92),
    "fog": (255, 207, 150, 72),
    "mid_trees": (36, 28, 31, 132),
    "shack": (22, 17, 15, 105),
    "foreground": (11, 12, 10, 165),
}
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


def create_placeholder_background_layer(layer_name):
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    surface.fill(BACKGROUND_PLACEHOLDER_COLORS[layer_name])
    return surface


def scale_background_layer(image, spec):
    width, height = image.get_size()

    if "width_ratio" in spec:
        target_width = int(SCREEN_WIDTH * spec["width_ratio"])
        scale = target_width / width
    else:
        scale = max(SCREEN_WIDTH / width, SCREEN_HEIGHT / height)

    scaled_size = (max(1, int(width * scale)), max(1, int(height * scale)))

    if scaled_size == image.get_size():
        return image

    return pygame.transform.smoothscale(image, scaled_size)


def load_background_layers():
    layers = []

    for spec in BACKGROUND_LAYER_SPECS:
        path = BACKGROUND_DIR / spec["filename"]
        if path.exists():
            image = pygame.image.load(path).convert_alpha()
        else:
            image = create_placeholder_background_layer(spec["name"])

        layers.append({
            "image": scale_background_layer(image, spec),
            "speed": spec["speed"],
            "drift": spec["drift"],
            "tile": spec["tile"],
            "align": spec.get("align", "top"),
            "spacing": spec.get("spacing"),
        })

    return layers


def get_background_layer_y(image, align):
    if align == "bottom":
        return SCREEN_HEIGHT - image.get_height()

    return 0


def draw_background_layer(screen, image, offset, tile, align, spacing=None):
    y = get_background_layer_y(image, align)

    if not tile:
        screen.blit(image, (0, y))
        return

    image_width = image.get_width()
    repeat_width = spacing or image_width
    start_x = -int(offset % repeat_width)
    x = start_x

    while x < SCREEN_WIDTH:
        screen.blit(image, (x, y))
        x += repeat_width


def draw_background(screen, background_layers, world_x, background_time):
    for layer in background_layers:
        offset = world_x * layer["speed"] + background_time * layer["drift"]
        draw_background_layer(
            screen,
            layer["image"],
            offset,
            layer["tile"],
            layer["align"],
            layer["spacing"],
        )


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
    background_layers = load_background_layers()

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

        draw_background(screen, background_layers, world_x, background_time)

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
