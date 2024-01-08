import pygame as pg
from pygame import Vector2

from tiled_map import TiledMap
from automata.manager import Manager


def main():
    pg.init()
    pg.display.set_mode((128, 128))
    tiled_map = TiledMap('assets/map/map.tmx')
    screen = pg.display.set_mode(tiled_map.px_size * 2 + Vector2(0, 500))
    map_size = screen.get_rect().size - Vector2(0, 500)
    manager = Manager()
    manager.update_plot()

    running = True
    clock = pg.time.Clock()
    while running:
        clock.tick(10)
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        manager.tick()
                        manager.update_plot()

        screen.fill((255, 255, 255, 255))
        tiled_map.renew_surface()
        manager.draw_predators(tiled_map)
        manager.draw_herbivores(tiled_map)
        manager.draw_scavengers(tiled_map)
        screen.blit(pg.transform.scale(tiled_map.surface, map_size), (0, 0))
        manager.draw_data(screen, pg.Rect((0, screen.get_size()[1] - 500, screen.get_size()[0], 500)))
        pg.display.flip()
        pg.display.update()


if __name__ == "__main__":
    main()
