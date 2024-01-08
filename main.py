import pygame as pg
from pygame.locals import RESIZABLE

from tiled_map import TiledMap
from automata.manager import Manager


def main():
    pg.init()
    pg.display.set_mode((128, 128))
    tiled_map = TiledMap('assets/map/map.tmx')
    screen = pg.display.set_mode(tiled_map.px_size * 1.5)
    manager = Manager()
    manager.draw_plot()

    running = True
    clock = pg.time.Clock()
    while running:
        clock.tick(30)
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        manager.tick()
                        manager.draw_plot()

        tiled_map.renew_surface()
        manager.draw_predators(tiled_map)
        manager.draw_herbivores(tiled_map)
        manager.draw_scavengers(tiled_map)
        tiled_map.draw_plot()
        screen.blit(pg.transform.scale(tiled_map.surface, screen.get_rect().size), (0, 0))
        pg.display.flip()
        pg.display.update()


if __name__ == "__main__":
    main()
