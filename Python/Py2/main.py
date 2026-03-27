import pygame
import random
from engine.config import *
from engine.map import GameMap, make_empty
from engine.player import Player
from engine.npc import NPC
from engine.sprites import build_sprite_sheet
from engine.palette import get_tileset

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 18)

# --- Build map ---
tiles = make_empty(20, 12, 0)
for x in range(20):
    tiles[0][x] = 1
    tiles[11][x] = 1
for y in range(12):
    tiles[y][0] = 1
    tiles[y][19] = 1

game_map = GameMap(tiles)

# --- Player ---
player_colors = {
    "skin": (241,194,125),
    "hair": (43,27,11),
    "shirt": (43,111,179),
    "pants": (58,43,27),
}
player_sheet = build_sprite_sheet(player_colors)
player = Player(game_map)

# --- NPCs ---
npc_list = []
npc_list.append(NPC("old", 12, 3, "Old Man", build_sprite_sheet({
    "skin": (241,194,125),
    "hair": (255,255,255),
    "shirt": (139,90,43),
    "pants": (58,43,27),
})))

npc_list.append(NPC("merchant", 9, 2, "Bob", build_sprite_sheet({
    "skin": (241,194,125),
    "hair": (43,27,11),
    "shirt": (58,108,255),
    "pants": (43,43,43),
}), npc_type="shop"))

# --- Dialog ---
dialog_open = False
dialog_text = ""

def open_dialog(text):
    global dialog_open, dialog_text
    dialog_open = True
    dialog_text = text

def close_dialog():
    global dialog_open
    dialog_open = False

# --- Main loop ---
world_time = 0
running = True

while running:
    dt = clock.tick(FPS) / 60.0
    world_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if dialog_open:
                    close_dialog()
                else:
                    # interact
                    pass

    keys = pygame.key.get_pressed()
    if not dialog_open:
        if keys[pygame.K_UP]: player.try_move(0, -1)
        elif keys[pygame.K_DOWN]: player.try_move(0, 1)
        elif keys[pygame.K_LEFT]: player.try_move(-1, 0)
        elif keys[pygame.K_RIGHT]: player.try_move(1, 0)

    player.update(dt)
    for npc in npc_list:
        npc.update_idle()
        npc.update_emotion()
        npc.update_wander(dt, world_time, game_map)

    # --- Draw ---
    screen.fill(COLOR_BG)

    # tiles
    for y in range(12):
        for x in range(20):
            t = tiles[y][x]
            color = (40,40,40) if t == 1 else (20,60,20)
            pygame.draw.rect(screen, color, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    player.draw(screen, player_sheet)

    for npc in npc_list:
        npc.draw(screen)

    # Dialog
    if dialog_open:
        pygame.draw.rect(screen, (0,0,0), (0, SCREEN_H-120, SCREEN_W, 120))
        pygame.draw.rect(screen, COLOR_ACCENT, (0, SCREEN_H-120, SCREEN_W, 120), 2)
        screen.blit(font.render(dialog_text, True, COLOR_TEXT), (20, SCREEN_H-100))

    pygame.display.flip()

pygame.quit()