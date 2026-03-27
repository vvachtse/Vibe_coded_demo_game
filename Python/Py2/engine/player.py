import pygame
from .config import TILE_SIZE

class Player:
    def __init__(self, game_map):
        self.map = game_map
        self.x = 2
        self.y = 2
        self.tx = 2
        self.ty = 2
        self.dir = 0
        self.moving = False
        self.progress = 0.0
        self.speed = 6.0
        self.frame = 0

    def try_move(self, dx, dy):
        if self.moving:
            return False

        tx = self.tx + dx
        ty = self.ty + dy

        # FIX: use map method
        if not self.map.can_walk(tx, ty):
            return False

        self.tx = tx
        self.ty = ty
        self.moving = True
        self.progress = 0.0

        if dy > 0: self.dir = 0
        elif dy < 0: self.dir = 3
        elif dx < 0: self.dir = 1
        elif dx > 0: self.dir = 2

        return True

    def update(self, dt):
        if self.moving:
            self.progress += self.speed * dt
            if self.progress >= 1.0:
                self.x = self.tx
                self.y = self.ty
                self.moving = False

    def draw(self, screen, sheet):
        if self.moving:
            px = self.x * TILE_SIZE
            py = self.y * TILE_SIZE
            tx = self.tx * TILE_SIZE
            ty = self.ty * TILE_SIZE
            t = min(self.progress, 1.0)
            x = px + (tx - px) * t
            y = py + (ty - py) * t
        else:
            x = self.x * TILE_SIZE
            y = self.y * TILE_SIZE

        frame = int((pygame.time.get_ticks() // 120) % 4)
        sx = frame * 16
        sy = self.dir * 24
        frame_surf = sheet.subsurface((sx, sy, 16, 24))
        frame_surf = pygame.transform.scale(frame_surf, (TILE_SIZE, TILE_SIZE))
        screen.blit(frame_surf, (x, y))