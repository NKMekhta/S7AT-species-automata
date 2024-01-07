from enum import Enum
from typing import Any

from .parameters import SharedParam


class Predator:
    class Config(Enum):
        POPULATION_LIMIT = 0
        INITIAL_POPULATION = 1
        INITIAL_SATURATION = 2
        INITIAL_ENERGY = 3
        INITIAL_STATE = 4

    class State(Enum):
        HUNTING_HERBIVORES = 0
        HUNTING_SCAVENGERS = 1
        EATING = 2
        SLEEPING = 3
        MULTIPLYING = 4
        INTERNAL_CONFLICT = 5

    class PrivateParam(Enum):
        # Before hunting
        HUNT_ACTIVELY = 4

        # After hunting
        MULTIPLY_AFTER_HUNT = 5
        HUNT_AGAIN = 6
        # Sleep otherwise

        # After multiplication and(or) conflict
        OVERCROWDING = 0
        SLEEP_NEEDED = 7
        # Hunt otherwise

        # After sleep
        SLEEP_AGAIN = 3
        MULTIPLY_AFTER_SLEEP = 8
        # Hunt otherwise

    config: dict[Config, Any] = {
        Config.POPULATION_LIMIT: 50,
        Config.INITIAL_SATURATION: 100,
        Config.INITIAL_POPULATION: 10,
        Config.INITIAL_ENERGY: 100,
        Config.INITIAL_STATE: State.SLEEPING
    }

    def __init__(self):
        self.population: int = self.config[self.Config.INITIAL_POPULATION]
        self.saturation: int = self.config[self.Config.INITIAL_SATURATION]
        self.energy: int = self.config[self.Config.INITIAL_ENERGY]
        self.state: Predator.State = self.config[self.Config.INITIAL_STATE]
        self.internal_params: dict[Predator.PrivateParam, bool] = {}

    def update(self, input_params: dict[SharedParam, bool]):
        self.__update_internals()
        ip = self.internal_params
        pp = self.PrivateParam
        sp = SharedParam
        st = self.State
        hunt_state = st.HUNTING_HERBIVORES if ip[pp.HUNT_ACTIVELY] else st.HUNTING_SCAVENGERS
        post_hunt_state = {
            ip[pp.HUNT_AGAIN]: hunt_state,
            ip[pp.MULTIPLY_AFTER_HUNT]: st.MULTIPLYING,
        }.setdefault(True, st.SLEEPING)

        match self.state:
            case self.State.EATING:
                self.state = post_hunt_state
            case self.State.SLEEPING:
                if ip[pp.SLEEP_AGAIN]:
                    self.state = st.SLEEPING
                elif ip[pp.MULTIPLY_AFTER_SLEEP]:
                    self.state = st.MULTIPLYING
                else:
                    self.state = hunt_state
            case self.State.HUNTING_HERBIVORES:
                if (not input_params.setdefault(sp.HERBIVORES_WILL_DEFEND, False)
                        and input_params.setdefault(sp.HERBIVORES_AVAILABLE, False)):
                    self.state = st.EATING
                else:
                    self.state = post_hunt_state
            case self.State.HUNTING_SCAVENGERS:
                self.state = st.EATING
            case self.State.MULTIPLYING:
                if ip[pp.OVERCROWDING]:
                    self.state = st.INTERNAL_CONFLICT
                elif ip[pp.SLEEP_NEEDED]:
                    self.state = st.SLEEPING
                else:
                    self.state = hunt_state
            case self.State.INTERNAL_CONFLICT:
                if ip[pp.SLEEP_NEEDED]:
                    self.state = st.SLEEPING
                else:
                    self.state = hunt_state
        self.__update_variables()

    def __update_internals(self):
        ip = self.internal_params
        pp = self.PrivateParam
        pop_limit = self.config[self.Config.POPULATION_LIMIT]

        ip[pp.OVERCROWDING] = self.population > pop_limit
        ip[pp.SLEEP_NEEDED] = self.energy < 10 or self.saturation >= 50
        ip[pp.HUNT_ACTIVELY] = self.energy >= 30
        ip[pp.HUNT_AGAIN] = self.energy >= 10 and self.saturation < 60
        ip[pp.MULTIPLY_AFTER_HUNT] = self.energy >= 30 and self.saturation >= 60
        ip[pp.MULTIPLY_AFTER_SLEEP] = self.energy >= 40 and self.saturation >= 50
        ip[pp.SLEEP_AGAIN] = self.energy < 40
        self.internal_params = ip

    def __update_variables(self):
        match self.state:
            case self.State.EATING:
                self.saturation += 60
            case self.State.SLEEPING:
                self.energy += 50
                self.saturation -= 2
            case self.State.HUNTING_HERBIVORES:
                self.energy -= 30
                self.saturation -= 5
            case self.State.HUNTING_SCAVENGERS:
                self.energy -= 10
                self.saturation -= 5
            case self.State.MULTIPLYING:
                self.population += 3
                self.energy -= 30
                self.saturation -= 10
            case self.State.INTERNAL_CONFLICT:
                self.population -= 10
                self.energy -= 40
                self.saturation -= 20

    def get_output(self) -> dict[SharedParam, bool]:
        return {
            SharedParam.PREDATOR_EATING: self.state == self.State.EATING,
            SharedParam.PREDATOR_HUNTING_HERBIVORES: self.state == self.State.HUNTING_HERBIVORES,
            SharedParam.PREDATOR_HUNTING_SCAVENGERS: self.state == self.State.HUNTING_SCAVENGERS,
        }
