import pygame
import math
import random
from .config import TILE_SIZE

class NPC:
    def __init__(self, npc_id, x, y, name, sprite_sheet, schedule=None, npc_type="npc"):
        self.id = npc_id
        self.x = x
        self.y = y
        self.dir = 0
        self.name = name
        self.sheet = sprite_sheet
        self.schedule = schedule
        self.type = npc_type

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
        self.bob = math.sin(self.idle_timer / 20) * 2

    def show_emotion(self, typ):
        self.emotion = typ
        self.emotion_timer = 60

    def update_emotion(self):
        if self.emotion_timer > 0:
            self.emotion_timer -= 1
            if self.emotion_timer <= 0:
                self.emotion = None

    def update_wander(self, dt, world_time, map_obj):
        is_day = int(world_time) % 40 < 20
        if self.schedule == "dayOnly" and not is_day:
            return

        self.wander_timer += dt
        if self.wander_timer > 2.5:
            self.wander_timer = 0
            dirs = [(0,-1,3),(0,1,0),(-1,0,1),(1,0,2)]
            dx, dy, ddir = random.choice(dirs)
            nx = self.x + dx
            ny = self.y + dy
            if map_obj.can_walk(nx, ny):
                self.x = nx
                self.y = ny
                self.dir = ddir

    def draw(self, screen):
        sx = self.x * TILE_SIZE
        sy = self.y * TILE_SIZE + self.bob

        frame = int((pygame.time.get_ticks() // 200) % 4)
        fx = frame * 16
        fy = self.dir * 24

        screen.blit(self.sheet, (sx, sy), (fx, fy, 16, 24))

        if self.emotion:
            pygame.draw.circle(screen, (255,255,255), (sx + TILE_SIZE//2, sy - 8), 8)
            font = pygame.font.SysFont("monospace", 14)
            screen.blit(font.render("!", True, (0,0,0)), (sx + TILE_SIZE//2 - 4, sy - 14))