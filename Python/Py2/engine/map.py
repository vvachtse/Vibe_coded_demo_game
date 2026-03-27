from .config import MAP_W, MAP_H

class GameMap:
    def __init__(self, tiles):
        self.tiles = tiles
        self.width = len(tiles[0])
        self.height = len(tiles)

    def can_walk(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
        if self.tiles[y][x] == 1:
            return False
        return True

def make_empty(w, h, fill=0):
    return [[fill for _ in range(w)] for _ in range(h)]