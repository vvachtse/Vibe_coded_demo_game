import pygame
from .config import TILE_PIX, TILESET_COLS
from .utils import hex_to_rgb

# Base indexed colors (same as JS)
BASE_INDEX_COLORS = {
    0: (0, 0, 0, 0),
    1: (34, 139, 34, 255),
    2: (107, 107, 107, 255),
    3: (196, 68, 68, 255),
    4: (139, 90, 43, 255),
    5: (255, 210, 77, 255),
    6: (0, 255, 255, 255),
    7: (58, 108, 255, 255),
}

# Same tile patterns as JS
INDEXED_TILES = [
    ["......",".1111.",".1..1.",".1..1.",".1111.","......"],
    ["......",".2222.",".2##2.",".2##2.",".2222.","......"],
    ["......","..333.",".3333.",".3..3.",".3333.","......"],
    ["......","..333.",".3333.",".3..3.",".3333.","......"],
    ["......","..111.",".1111.",".1111.","..444.","......"],
    ["......","..555.",".5555.",".5555.","..555.","......"],
    ["......","..666.",".6666.",".6666.",".6666.","......"],
    ["......",".7777.",".7..7.",".7..7.",".7777.","......"],
]

PALETTES = {
    "default": {1:"#3cb043",2:"#6b6b6b",3:"#c44",4:"#8b5a2b",5:"#ffd24d",6:"#0ff",7:"#3a6cff"},
    "night":   {1:"#2a5f2a",2:"#3a3a3a",3:"#6b2a2a",4:"#5a3f2a",5:"#e6c94d",6:"#0aa",7:"#1f3f7f"},
    "desert":  {1:"#c9b97a",2:"#8b7a6b",3:"#b24a2a",4:"#7a5a2a",5:"#ffd24d",6:"#7ad",7:"#b0d0ff"},
    "snow":    {1:"#cfead6",2:"#bdbdbd",3:"#a84a4a",4:"#8b6b5a",5:"#fff1b0",6:"#bff",7:"#cfe6ff"},
}

class TileSet:
    def __init__(self):
        self.index_surface = self.build_indexed_tiles()
        self.cache = {}

    def build_indexed_tiles(self):
        w = TILESET_COLS * TILE_PIX
        h = 2 * TILE_PIX
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        for i, grid in enumerate(INDEXED_TILES):
            col = i % TILESET_COLS
            row = i // TILESET_COLS
            ox = col * TILE_PIX
            oy = row * TILE_PIX

            for r, line in enumerate(grid):
                for c, ch in enumerate(line):
                    if ch == ".":
                        continue
                    if ch == "#":
                        continue  # skip placeholder pixels

                    idx = int(ch)  # now guaranteed safe
                    rgba = BASE_INDEX_COLORS[idx]
                    surf.set_at((ox + c, oy + r), rgba)

        return surf

    def recolor(self, palette_name):
        if palette_name in self.cache:
            return self.cache[palette_name]

        pal = PALETTES.get(palette_name, PALETTES["default"])
        src = self.index_surface
        w, h = src.get_size()
        out = pygame.Surface((w, h), pygame.SRCALPHA)

        for y in range(h):
            for x in range(w):
                r, g, b, a = src.get_at((x, y))
                if a == 0:
                    continue

                matched = None
                for idx, col in BASE_INDEX_COLORS.items():
                    if col[:3] == (r, g, b):
                        matched = idx
                        break

                if matched is None:
                    out.set_at((x, y), (r, g, b, a))
                else:
                    hexcol = pal.get(matched)
                    if hexcol:
                        nr, ng, nb = hex_to_rgb(hexcol)
                        out.set_at((x, y), (nr, ng, nb, 255))
                    else:
                        out.set_at((x, y), (r, g, b, a))

        self.cache[palette_name] = out
        return out