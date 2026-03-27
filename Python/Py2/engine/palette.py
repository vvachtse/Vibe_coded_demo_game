from .tiles import TileSet

tileset = TileSet()

def get_tileset(palette_name):
    return tileset.recolor(palette_name)