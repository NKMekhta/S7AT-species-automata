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
        self.surface = pg.Surface(self.px_size + 2 * self.tl_size, pg.SRCALPHA, 32).convert_alpha()
        self.aspect_ratio = self.surface.get_size()[0] / self.surface.get_size()[1]

    def renew_surface(self):
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    if tile:
                        self.draw_at(
                            img=tile,
                            dest=(x, y),
                            align=(0.5, 1)
                        )

    def draw_at(self
                , img: Surface
                , dest: tuple[float, float]
                , scale: Optional[float] = None
                , aspect_ratio: Optional[float] = None
                , area: Optional[pg.Rect] = None
                , flip: tuple[bool, bool] = (False, False)
                , align: tuple[float, float] = (0.5, 0.5)) -> None:

        # Scale
        if scale is not None:
            sprite_size = self.tl_size * scale
        else:
            sprite_size = Vector2(img.get_size())

        # Crop
        if area is not None:
            crop = Surface(area.size, pg.SRCALPHA)
            crop.blit(img, (0, 0), area)
            img = crop

        # Flip
        img = pg.transform.flip(img, *flip)

        # Fit
        if aspect_ratio is None:
            aspect_ratio = img.get_size()[0] / img.get_size()[1]
        if sprite_size.y * aspect_ratio > sprite_size.x:
            sprite_size.y = sprite_size.x / aspect_ratio
        else:
            sprite_size.x = sprite_size.y * aspect_ratio

        # Calculate position
        (x, y) = dest
        screen_x = (x - y) * self.tl_size.x // 2 + self.px_size.x / 2
        screen_y = (x + y) * self.tl_size.y // 4

        # Align
        screen_x -= (sprite_size.x - self.tl_size.x) * align[0]
        screen_y -= (sprite_size.y - self.tl_size.y) * align[1]

        self.surface.blit(pg.transform.scale(img, sprite_size), (screen_x, screen_y))
