from math import ceil
from typing import Optional

import pygame as pg
import pytmx
from pygame import Vector2, Surface


class TiledMap:
    def __init__(self, filename):
        self.tmxdata = tm = pytmx.load_pygame(filename)
        self.px_size = Vector2(tm.width * tm.tilewidth, tm.height * tm.tileheight + 300)
        self.tl_size = Vector2(tm.tilewidth, tm.tileheight * 2)
        self.mp_size = Vector2(tm.width, tm.height)
        self.surface = pg.Surface(self.px_size + 2 * self.tl_size, pg.SRCALPHA, 32).convert_alpha()
        self.aspect_ratio = self.surface.get_size()[0] / self.surface.get_size()[1]

    def renew_surface(self):
        self.surface.fill((0, 0, 0, 0))
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        self.draw_at(tile, (x, y))

    def draw_at(self
                , img: Surface
                , dest: tuple[float, float]
                , scale: float = 1
                , aspect_ratio: Optional[float] = None
                , area: Optional[pg.Rect] = None
                , flip: tuple[bool, bool] = (False, False)):
        if area is not None:
            crop = Surface(area.size, pg.SRCALPHA)
            crop.blit(img, (0, 0), area)
            img = crop
        img = pg.transform.flip(img, *flip)
        if aspect_ratio is None:
            aspect_ratio = img.get_size()[0] / img.get_size()[1]
        sprite_size = self.tl_size * scale
        if sprite_size.y * aspect_ratio > sprite_size.x:
            sprite_size.y = sprite_size.x / aspect_ratio
        else:
            sprite_size.x = sprite_size.y * aspect_ratio
        (x, y) = dest

        screen_x = (x - y) * self.tl_size.x // 2 + self.px_size.x / 2 + self.tl_size.x
        screen_x -= (sprite_size.x - self.tl_size.x) / 2
        screen_y = (x + y) * self.tl_size.y // 4 + self.tl_size.y
        screen_y -= (sprite_size.y - self.tl_size.y) / 2
        self.surface.blit(pg.transform.scale(img, sprite_size), (screen_x, screen_y))

    def draw_plot(self):
        try:
            img = pg.image.load('tmp.png')
            dest = self.surface.get_size()
            self.surface.blit(pg.transform.scale(img, (dest[0], 300)), (0, dest[1] - 300))
        except:
            pass
