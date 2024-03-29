import pygame as pg
import matplotlib.pyplot as plt
from pygame import Vector2

from automata.predator import Predator
from automata.herbivore import Herbivore
from automata.scavenger import Scavenger
from tiled_map import TiledMap


class Manager:
    def __init__(self):
        self.predator = Predator()
        self.herbivore = Herbivore()
        self.scavenger = Scavenger()
        self.predator_sprite_sheet = pg.image.load("assets/sprites/trex_states.png").convert_alpha()
        self.herbivore_sprite_sheet = pg.image.load("assets/sprites/triceratops_states.png").convert_alpha()
        self.scavenger_sprite_sheet = pg.image.load("assets/sprites/raptor_states.png").convert_alpha()
        self.meat = pg.image.load("assets/sprites/anonymous_meat.png").convert_alpha()
        self.scavenger_history = [0] * 16
        self.herbivore_history = [0] * 16
        self.predator_history = [0] * 16
        self.counter = 0

    def tick(self):
        self.counter += 1
        outputs = self.predator.get_output() | self.herbivore.get_output() | self.scavenger.get_output()
        self.predator.update(outputs)
        self.herbivore.update(outputs)
        self.scavenger.update(outputs)
        self.predator_history.append(self.predator.population)
        self.predator_history.pop(0)
        self.scavenger_history.append(self.scavenger.population)
        self.scavenger_history.pop(0)
        self.herbivore_history.append(self.herbivore.population)
        self.herbivore_history.pop(0)

    def draw_predators(self, tiled_map: TiledMap):
        st = Predator.State
        aspect_ratio = 1.5
        height = 32
        width = 48
        scale = 2
        match self.predator.state:
            case st.SLEEPING:
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (2, 2), scale, aspect_ratio,
                    pg.Rect(0, height * 2, width, height)
                )
            case st.EATING:
                tiled_map.draw_at(
                    self.meat,
                    (4.2, 5.8)
                )
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (5, 5), scale, aspect_ratio,
                    pg.Rect(0, height, width, height)
                )
            case st.MULTIPLYING:
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (2, 3), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                )
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (2, 2), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height)
                )
            case st.INTERNAL_CONFLICT:
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (1, 3), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                    (True, False)
                )
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (3, 1), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                )
            case st.HUNTING_HERBIVORES:
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (5, 7), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                )
            case st.HUNTING_SCAVENGERS:
                tiled_map.draw_at(
                    self.predator_sprite_sheet,
                    (10, 8), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                )

    def draw_herbivores(self, tiled_map: TiledMap):
        st = Herbivore.State
        aspect_ratio = 1.5
        width = 48
        height = 32
        scale = 1.5
        match self.herbivore.state:
            case st.SLEEPING:
                tiled_map.draw_at(
                    self.herbivore_sprite_sheet,
                    (0, 12), scale, aspect_ratio,
                    pg.Rect(0, height * 3, width, height),
                    (True, False),
                )
            case st.EATING:
                tiled_map.draw_at(
                    self.herbivore_sprite_sheet,
                    (1, 12), scale, aspect_ratio,
                    pg.Rect(0, height, width, height)
                )
            case st.MULTIPLYING:
                tiled_map.draw_at(
                    self.herbivore_sprite_sheet,
                    (2, 10), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                    (True, False)
                )
                tiled_map.draw_at(
                    self.herbivore_sprite_sheet,
                    (1.5, 9.8), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                    (True, False)
                )
            case st.MIGRATING:
                tiled_map.draw_at(
                    self.herbivore_sprite_sheet,
                    (3, 13), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                    (True, False)
                )
            case st.DEFENDING:
                tiled_map.draw_at(
                    self.herbivore_sprite_sheet,
                    (4, 10), scale, aspect_ratio,
                    pg.Rect(0, height * 2, width, height),
                    (True, False)
                )
            case st.ESCAPING:
                tiled_map.draw_at(
                    self.herbivore_sprite_sheet,
                    (3, 10), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                )

    def draw_scavengers(self, tiled_map: TiledMap):
        st = Scavenger.State
        aspect_ratio = 1
        width = 32
        height = 32
        scale = 1
        sprite_sheet = self.scavenger_sprite_sheet
        match self.scavenger.state:
            case st.SLEEPING:
                tiled_map.draw_at(
                    sprite_sheet,
                    (12, 12), scale, aspect_ratio,
                    pg.Rect(0, height * 3, width, height),
                    (True, False),
                )
            case st.EATING:
                tiled_map.draw_at(
                    self.meat,
                    (4.2, 5.8),
                )
                tiled_map.draw_at(
                    sprite_sheet,
                    (5, 5), scale, aspect_ratio,
                    pg.Rect(0, height * 2, width, height),
                )
            case st.MULTIPLYING:
                tiled_map.draw_at(
                    sprite_sheet,
                    (12, 12), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                    (True, False)
                )
                tiled_map.draw_at(
                    sprite_sheet,
                    (11.8, 12.5), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                    (True, False)
                )
            case st.HIDING:
                tiled_map.draw_at(
                    sprite_sheet,
                    (13, 13), scale, aspect_ratio,
                    pg.Rect(0, height, width, height),
                )
            case st.WANDERING:
                tiled_map.draw_at(
                    sprite_sheet,
                    (9.5, 4.5), scale, aspect_ratio,
                    pg.Rect(0, 0, width, height),
                    (True, False)
                )
            case st.CANNIBALISM:
                tiled_map.draw_at(
                    sprite_sheet,
                    (12, 12), scale, aspect_ratio,
                    pg.Rect(0, height * 3, width, height),
                )
                tiled_map.draw_at(
                    sprite_sheet,
                    (12.5, 11.5), scale, aspect_ratio,
                    pg.Rect(0, height * 2, width, height),
                )

    def update_plot(self):
        plt.clf()
        plt.plot(range(self.counter, self.counter + 16), self.scavenger_history, color='blue', label='Scavengers')
        plt.plot(range(self.counter, self.counter + 16), self.herbivore_history, color='green', label='Herbivores')
        plt.plot(range(self.counter, self.counter + 16), self.predator_history, color='red', label='Predators')
        plt.savefig('tmp')

    def draw_data(self, surface: pg.Surface, rect: pg.Rect):
        try:
            img = pg.image.load('tmp.png')
            dest = Vector2(surface.get_size()[0] - img.get_size()[0], rect.y)
            surface.blit(img, dest)
        except:
            pass

        font = pg.font.Font(size=28)
        text = (
            f'\nTick {self.counter}'
            + '\nPredator:'
            + f'\n    {self.predator.state}'
            + f'\n    e: {self.predator.energy}'
            + f'\n    s: {self.predator.saturation}'
            + f'\n    p: {self.predator.population}'
            + '\nHerbivore'
            + f'\n    {self.herbivore.state}'
            + f'\n    e: {self.herbivore.energy}'
            + f'\n    s: {self.herbivore.saturation}'
            + f'\n    p: {self.herbivore.population}'
            + '\nScavenger'
            + f'\n    {self.scavenger.state}'
            + f'\n    e: {self.scavenger.energy}'
            + f'\n    s: {self.scavenger.saturation}'
            + f'\n    p: {self.scavenger.population}'
        )
        render = font.render(text, False, (0, 0, 0, 255))
        dest = Vector2(rect.x, rect.y)
        surface.blit(render, dest)
