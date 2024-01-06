from math import ceil
from typing import Optional

import pygame as pg
import pytmx
from pygame import Vector2, Surface


class TiledMap:
    def __init__(self, filename):
        self.tmxdata = tm = pytmx.load_pygame(filename)
        self.px_size = Vector2(tm.width * tm.tilewidth, tm.height * tm.tileheight)
        self.tl_size = Vector2(tm.tilewidth, tm.tileheight * 2)
        self.mp_size = Vector2(tm.width, tm.height)
        self.surface = pg.Surface(self.px_size + 2 * self.tl_size)
        self. aspect_ratio = self.surface.get_size()[0] / self.surface.get_size()[1]

    def renew_surface(self):
        self.surface.fill((0, 0, 0, 255))
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        self.draw_at(tile, (x, y))

    def draw_at(self, img: Surface, dest: tuple[float, float], scale: float = 1, aspect_ratio: Optional[float] = None):
        if aspect_ratio is None:
            aspect_ratio = img.get_size()[0] / img.get_size()[1]
        max_dims = self.tl_size * scale
        if max_dims.y * aspect_ratio > max_dims.x:
            max_dims.y = max_dims.x / aspect_ratio
        else:
            max_dims.x = max_dims.y * aspect_ratio
        (x, y) = dest

        screen_x = (x - y) * self.tl_size.x // 2 + self.px_size.x / 2 + self.tl_size.x
        screen_y = (x + y) * self.tl_size.y // 4 + self.tl_size.y
        self.surface.blit(pg.transform.scale(img, self.tl_size), (screen_x, screen_y))

    def get_surface(self):
        return self.surface
