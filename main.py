import pygame as pg
from pygame.locals import FULLSCREEN

from tiled_map import TiledMap
from automaton_manager import Manager

def main():
    pg.init()
    screen = pg.display.set_mode((128, 128), FULLSCREEN)
    character_sprite = pg.image.load('assets/dante.jpg')
    tiled_map = TiledMap('assets/map/map.tmx')
    manager = Manager()

    running = True
    while running:
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case pg.locals.VIDEORESIZE:
                    screen = pg.display.set_mode((
                        event.size[0],
                        event.size[0] / tiled_map.aspect_ratio
                    ))
                case pg.K_SPACE:
                    manager.tick()

        tiled_map.renew_surface()
        tiled_map.draw_at(character_sprite, (2, 2), 4)
        tiled_map.draw_at(character_sprite, (10, 10))
        tiled_map.draw_at(character_sprite, (2, 10))
        screen.blit(pg.transform.scale(tiled_map.get_surface(), screen.get_rect().size), (0, 0))
        pg.display.flip()


if __name__ == "__main__":
    main()
