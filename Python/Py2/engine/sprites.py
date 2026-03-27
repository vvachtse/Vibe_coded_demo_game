import pygame
from .config import FRAME_W, FRAME_H, SHEET_COLS, SHEET_ROWS

FRAME_W = 16
FRAME_H = 24
SHEET_COLS = 4
SHEET_ROWS = 4

def draw_base_sprite(ctx, frame, direction, colors):
    ctx.fill((0, 0, 0, 0))
    # head
    pygame.draw.rect(ctx, colors["skin"], (6, 2, 4, 4))
    pygame.draw.rect(ctx, colors["hair"], (6, 1, 4, 1))
    # shirt
    pygame.draw.rect(ctx, colors["shirt"], (5, 6, 6, 6))
    # legs
    pygame.draw.rect(ctx, colors["pants"], (5, 12, 3, 3))
    pygame.draw.rect(ctx, colors["pants"], (8, 12, 3, 3))

    arm_offset = -1 if frame % 2 == 0 else 1
    if direction == 0:  # down
        pygame.draw.rect(ctx, colors["skin"], (4 + arm_offset, 7, 2, 4))
        pygame.draw.rect(ctx, colors["skin"], (10 - arm_offset, 7, 2, 4))
    elif direction == 3:  # up
        pygame.draw.rect(ctx, colors["skin"], (4 + arm_offset, 4, 2, 4))
        pygame.draw.rect(ctx, colors["skin"], (10 - arm_offset, 4, 2, 4))
    else:  # left/right
        pygame.draw.rect(ctx, colors["skin"], (4, 7, 2, 4))
        pygame.draw.rect(ctx, colors["skin"], (10, 7, 2, 4))

def build_sprite_sheet(colors):
    sheet = pygame.Surface((FRAME_W * SHEET_COLS, FRAME_H * SHEET_ROWS), pygame.SRCALPHA)
    for direction in range(SHEET_ROWS):
        for frame in range(SHEET_COLS):
            tmp = pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)
            draw_base_sprite(tmp, frame, direction, colors)
            sheet.blit(tmp, (frame * FRAME_W, direction * FRAME_H))
    return sheet