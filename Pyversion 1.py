import pygame
import random
import math
import sys

pygame.init()

# --- Config ---
TILE = 48
MAP_W, MAP_H = 20, 12
SCREEN_W, SCREEN_H = MAP_W * TILE, MAP_H * TILE + 120  # extra space for UI
FPS = 60

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Retro RPG — Pygame Version")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 18)

# --- Colors ---
BLACK = (7, 16, 24)
PANEL = (0, 0, 0)
ACCENT = (255, 210, 77)
TEXT = (234, 234, 234)
MUTED = (154, 163, 178)
RED = (196, 68, 68)
GREEN = (60, 176, 67)
GRAY = (107, 107, 107)
BROWN = (139, 90, 43)
BLUE = (58, 108, 255)

# --- Map ---
def make_empty(w, h, fill=0):
    return [[fill for _ in range(w)] for _ in range(h)]

tiles = make_empty(MAP_W, MAP_H, 0)
# Borders as walls (1)
for x in range(MAP_W):
    tiles[0][x] = 1
    tiles[MAP_H - 1][x] = 1
for y in range(MAP_H):
    tiles[y][0] = 1
    tiles[y][MAP_W - 1] = 1

# Some decorative tiles
tiles[2][6] = 2
tiles[2][7] = 2
tiles[3][6] = 2
tiles[3][7] = 2
tiles[6][14] = 7
tiles[6][15] = 7

# --- Player ---
player = {
    "x": 2,
    "y": 2,
    "tx": 2,
    "ty": 2,
    "dir": 0,  # 0 down, 1 left, 2 right, 3 up
    "moving": False,
    "move_progress": 0.0,
    "speed": 6.0,
    "hp": 30,
    "max_hp": 30,
}

# --- NPCs ---
class NPC:
    def __init__(self, npc_id, x, y, name, color, schedule=None, npc_type="npc"):
        self.id = npc_id
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.schedule = schedule
        self.type = npc_type
        self.dir = 0
        self.idle_timer = 0
        self.blink = 0
        self.bob = 0.0
        self.wander_timer = 0.0
        self.emotion = None
        self.emotion_timer = 0

    def update_idle(self):
        self.idle_timer += 1
        if self.idle_timer % 180 == 0:
            self.blink = 6
        if self.blink > 0:
            self.blink -= 1
        self.bob = math.sin(self.idle_timer / 20.0) * 3

    def show_emotion(self, typ):
        self.emotion = typ
        self.emotion_timer = 60

    def update_emotion(self):
        if self.emotion_timer > 0:
            self.emotion_timer -= 1
            if self.emotion_timer <= 0:
                self.emotion = None

    def update_wander(self, dt, world_time):
        # simple day/night toggle
        is_day = int(world_time) % 40 < 20
        if self.schedule == "dayOnly" and not is_day:
            return
        self.wander_timer += dt
        if self.wander_timer > 2.5:
            self.wander_timer = 0
            dirs = [
                (0, -1, 3),
                (0, 1, 0),
                (-1, 0, 1),
                (1, 0, 2),
            ]
            dx, dy, ddir = random.choice(dirs)
            nx = self.x + dx
            ny = self.y + dy
            if 0 <= nx < MAP_W and 0 <= ny < MAP_H and tiles[ny][nx] != 1:
                self.x = nx
                self.y = ny
                self.dir = ddir

npcs = [
    NPC("obj_old", 12, 3, "Old Man", ACCENT),
    NPC("merchant_1", 9, 2, "Bob", (122, 173, 255), npc_type="shop"),
    NPC("guard_1", 5, 5, "Guard", BLUE, schedule="dayOnly"),
    NPC("villager_1", 7, 7, "Lina", (85, 170, 85)),
    NPC("wizard_1", 3, 3, "Sage", (153, 51, 204)),
    NPC("child_1", 15, 4, "Kid", (255, 102, 102)),
]

# --- Events (simplified) ---
events = {
    "obj_old": [{"type": "dialog", "text": "Old man: 'Beware the forest.'"}],
    "merchant_1": [{"type": "dialog", "text": "Merchant: 'Welcome! (shop not implemented yet)'"}],
    "guard_1": [{"type": "dialog", "text": "Guard: 'I only patrol during the day.'"}],
    "villager_1": [{"type": "dialog", "text": "Lina: 'Nice weather, huh?'"}],
    "wizard_1": [{"type": "dialog", "text": "Sage: 'The world shifts with time...'"}],
    "child_1": [{"type": "dialog", "text": "Kid: 'Catch me if you can!'"}],
}

# --- Dialog / Battle state ---
dialog_open = False
dialog_text = ""
dialog_queue = []
battle = None  # None or dict

def open_dialog(text, more=None):
    global dialog_open, dialog_text, dialog_queue
    dialog_open = True
    dialog_text = text
    dialog_queue = more or []

def close_dialog():
    global dialog_open, dialog_text, dialog_queue
    if dialog_queue:
        dialog_text = dialog_queue.pop(0)
    else:
        dialog_open = False
        dialog_text = ""

def run_events_for(npc_id):
    acts = events.get(npc_id)
    if not acts:
        return
    texts = [a["text"] for a in acts if a["type"] == "dialog"]
    if texts:
        open_dialog(texts[0], texts[1:])

# --- Battle ---
def start_wild_encounter():
    global battle
    enemy = {
        "name": random.choice(["Twiglet", "Mudkin"]),
        "level": random.randint(3, 5),
        "hp": 24,
        "max_hp": 24,
    }
    battle = {
        "enemy": enemy,
        "log": [f"A wild {enemy['name']} appeared!"],
    }

def end_battle():
    global battle
    battle = None

# --- Movement & collision ---
def can_walk(x, y):
    if x < 0 or y < 0 or x >= MAP_W or y >= MAP_H:
        return False
    if tiles[y][x] == 1:
        return False
    return True

def try_move(dx, dy):
    if player["moving"] or dialog_open or battle:
        return
    tx = player["tx"] + dx
    ty = player["ty"] + dy
    if not can_walk(tx, ty):
        return
    player["tx"] = tx
    player["ty"] = ty
    player["moving"] = True
    player["move_progress"] = 0.0
    if dy > 0:
        player["dir"] = 0
    elif dy < 0:
        player["dir"] = 3
    elif dx < 0:
        player["dir"] = 1
    elif dx > 0:
        player["dir"] = 2

    # random encounter (1/20)
    if random.randint(1, 20) == 1:
        start_wild_encounter()

def update_player(dt):
    if player["moving"]:
        player["move_progress"] += player["speed"] * dt
        if player["move_progress"] >= 1.0:
            player["x"] = player["tx"]
            player["y"] = player["ty"]
            player["moving"] = False

# --- Rendering ---
def draw_map():
    for y in range(MAP_H):
        for x in range(MAP_W):
            t = tiles[y][x]
            if t == 0:
                color = (20, 60, 20)
            elif t == 1:
                color = (40, 40, 40)
            elif t == 2:
                color = (120, 120, 120)
            elif t == 7:
                color = (80, 120, 220)
            else:
                color = (60, 60, 60)
            pygame.draw.rect(screen, color, (x * TILE, y * TILE, TILE, TILE))

def draw_player():
    if player["moving"]:
        px = player["x"] * TILE
        py = player["y"] * TILE
        tx = player["tx"] * TILE
        ty = player["ty"] * TILE
        t = min(player["move_progress"], 1.0)
        x = px + (tx - px) * t
        y = py + (ty - py) * t
    else:
        x = player["x"] * TILE
        y = player["y"] * TILE

    pygame.draw.rect(screen, (240, 200, 120), (x + 12, y + 4, TILE - 24, TILE - 16))

def draw_npcs():
    for npc in npcs:
        npc.update_idle()
        npc.update_emotion()
        sx = npc.x * TILE
        sy = npc.y * TILE + npc.bob
        pygame.draw.rect(screen, npc.color, (sx + 12, sy + 4, TILE - 24, TILE - 16))
        # emotion bubble
        if npc.emotion:
            pygame.draw.circle(screen, (255, 255, 255), (sx + TILE // 2, int(sy) - 8), 8)
            txt = font.render("!", True, (0, 0, 0))
            screen.blit(txt, (sx + TILE // 2 - 4, int(sy) - 14))

def draw_dialog():
    if not dialog_open:
        return
    h = 100
    y = SCREEN_H - h
    pygame.draw.rect(screen, (0, 0, 0), (0, y, SCREEN_W, h))
    pygame.draw.rect(screen, ACCENT, (0, y, SCREEN_W, h), 2)
    lines = []
    text = dialog_text
    while len(text) > 0:
        lines.append(text[:50])
        text = text[50:]
    for i, line in enumerate(lines[:3]):
        surf = font.render(line, True, TEXT)
        screen.blit(surf, (16, y + 16 + i * 24))

def draw_battle():
    if not battle:
        return
    pygame.draw.rect(screen, (0, 0, 0), (40, 40, SCREEN_W - 80, SCREEN_H - 160))
    pygame.draw.rect(screen, ACCENT, (40, 40, SCREEN_W - 80, SCREEN_H - 160), 2)
    enemy = battle["enemy"]
    title = font.render(f"{enemy['name']} (L{enemy['level']})", True, TEXT)
    screen.blit(title, (60, 60))
    # HP bar
    hp_ratio = max(0, enemy["hp"] / enemy["max_hp"])
    pygame.draw.rect(screen, (60, 60, 60), (60, 90, 200, 16))
    pygame.draw.rect(screen, RED, (60, 90, int(200 * hp_ratio), 16))
    # log
    log_y = 130
    for line in battle["log"][-5:]:
        surf = font.render(line, True, TEXT)
        screen.blit(surf, (60, log_y))
        log_y += 22
    hint = font.render("Press Z to attack, X to run", True, MUTED)
    screen.blit(hint, (60, SCREEN_H - 140))

# --- Input helpers ---
def interact():
    if dialog_open:
        close_dialog()
        return
    if battle:
        return
    # check NPC in front of player
    dx, dy = 0, 0
    if player["dir"] == 0:
        dy = 1
    elif player["dir"] == 3:
        dy = -1
    elif player["dir"] == 1:
        dx = -1
    elif player["dir"] == 2:
        dx = 1
    tx = player["x"] + dx
    ty = player["y"] + dy
    for npc in npcs:
        if npc.x == tx and npc.y == ty:
            npc.show_emotion("!")
            run_events_for(npc.id)
            break

def battle_attack():
    if not battle:
        return
    enemy = battle["enemy"]
    dmg = random.randint(4, 8)
    enemy["hp"] = max(0, enemy["hp"] - dmg)
    battle["log"].append(f"You hit {enemy['name']} for {dmg}!")
    if enemy["hp"] <= 0:
        battle["log"].append(f"{enemy['name']} fainted!")
        pygame.time.set_timer(pygame.USEREVENT + 1, 600, loops=1)

def battle_run():
    if not battle:
        return
    if random.random() < 0.6:
        battle["log"].append("You ran away!")
        pygame.time.set_timer(pygame.USEREVENT + 1, 400, loops=1)
    else:
        battle["log"].append("Couldn't escape!")

# --- Main loop ---
world_time = 0.0
running = True
while running:
    dt = clock.tick(FPS) / 60.0
    world_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:
            end_battle()

    keys = pygame.key.get_pressed()
    if not dialog_open and not battle:
        if keys[pygame.K_UP]:
            try_move(0, -1)
        elif keys[pygame.K_DOWN]:
            try_move(0, 1)
        elif keys[pygame.K_LEFT]:
            try_move(-1, 0)
        elif keys[pygame.K_RIGHT]:
            try_move(1, 0)

    for event in pygame.event.get():
        pass  # already handled above; avoid double loop in real code

    # single keydown handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if battle:
                    battle_attack()
                else:
                    interact()
            elif event.key == pygame.K_x:
                if battle:
                    battle_run()
                else:
                    # could open menu here
                    pass

    update_player(dt)
    for npc in npcs:
        npc.update_wander(dt, world_time)

    screen.fill(BLACK)
    draw_map()
    draw_npcs()
    draw_player()
    if battle:
        draw_battle()
    draw_dialog()

    pygame.display.flip()

pygame.quit()
sys.exit()