from typing import Any
import pygame as pg

from automaton import Predator, SharedParam
from tiled_map import TiledMap


class Manager:
    def __init__(self):
        self.predator = Predator()
        predator_sprite_sheet = pg.image.load("assets/sprites/trex_states.png")
        predator_sprites = [
            predator_sprite_sheet.blit(predator_sprite_sheet, (0, 0), (0, 0, 32 * i, 48)) for i in range(3)
        ]
        self.predator_sprites: dict[Predator.State, Any] = {
            Predator.State.SLEEPING: predator_sprites[2],
            Predator.State.HUNTING_HERBIVORES: predator_sprites[0],
            Predator.State.HUNTING_SCAVENGERS: predator_sprites[0],
            Predator.State.EATING: predator_sprites[1],
            Predator.State.MULTIPLYING: predator_sprites[0],
            Predator.State.INTERNAL_CONFLICT: predator_sprites[0],
        }

    def tick(self):
        outputs = self.predator.get_output()
        self.predator.update(outputs)
        print(self.predator)

    def draw_predators(self, map: TiledMap):
        st = Predator.State
        active_sprite = self.predator_sprites[self.predator.state]
        # match self.predator.state:
        #     case st.SLEEPING:
        #         map.draw_at()
