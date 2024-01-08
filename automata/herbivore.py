from enum import Enum
from typing import Any

from .parameters import SharedParam


class Herbivore:
    class Config(Enum):
        INITIAL_POPULATION = 1
        INITIAL_SATURATION = 2
        INITIAL_ENERGY = 3
        INITIAL_STATE = 4
        AVAILABILITY_THRESHOLD = 5

    class State(Enum):
        DEFENDING = 0
        ESCAPING = 1
        EATING = 2
        SLEEPING = 3
        MULTIPLYING = 4
        MIGRATING = 5

    class PrivateParam(Enum):
        HAS_ENERGY_TO_DEFEND = 0
        SHOULD_SLEEP = 1
        SHOULD_GRAZE = 2
        SHOULD_MULTIPLY = 3
        OVERCROWDING = 4

    config: dict[Config, Any] = {
        Config.INITIAL_SATURATION: 100,
        Config.INITIAL_POPULATION: 30,
        Config.INITIAL_ENERGY: 100,
        Config.INITIAL_STATE: State.SLEEPING,
        Config.AVAILABILITY_THRESHOLD: 15,
    }

    def __init__(self):
        self.population: int = self.config[self.Config.INITIAL_POPULATION]
        self.saturation: int = self.config[self.Config.INITIAL_SATURATION]
        self.energy: int = self.config[self.Config.INITIAL_ENERGY]
        self.state: Herbivore.State = self.config[self.Config.INITIAL_STATE]
        self.internal_params: dict[Herbivore.PrivateParam, bool] = {}
        self.__update_internals()

    def update(self, input_params: dict[SharedParam, bool]):
        self.__update_internals()
        ip = self.internal_params
        pp = self.PrivateParam
        sp = SharedParam
        st = self.State

        if input_params[sp.PREDATOR_HUNTING_HERBIVORES]:
            if ip[pp.HAS_ENERGY_TO_DEFEND]:
                self.state = st.DEFENDING
            else:
                self.state = st.ESCAPING
        else:
            self.state = {
                ip[pp.SHOULD_GRAZE]: st.EATING,
                ip[pp.SHOULD_MULTIPLY] and not ip[pp.OVERCROWDING]: st.MULTIPLYING,
                ip[pp.SHOULD_SLEEP]: st.SLEEPING,
            }.setdefault(True, st.MIGRATING)
        self.__update_variables()

    def __update_internals(self):
        ip = self.internal_params
        pp = self.PrivateParam
        ip[pp.HAS_ENERGY_TO_DEFEND] = self.energy >= 60
        ip[pp.SHOULD_GRAZE] = self.energy >= 10 and self.saturation < 60
        ip[pp.SHOULD_SLEEP] = self.energy < 10
        ip[pp.SHOULD_MULTIPLY] = self.energy >= 30 and 60 <= self.saturation <= 100
        ip[pp.OVERCROWDING] = self.population >= self.config[self.Config.AVAILABILITY_THRESHOLD] * 10
        self.internal_params = ip

    def __update_variables(self):
        match self.state:
            case self.State.EATING:
                self.saturation += 50
                self.energy -= 5
            case self.State.SLEEPING:
                self.energy += 50
                self.saturation -= 10
            case self.State.MIGRATING:
                self.energy -= 5
                self.saturation -= 20
            case self.State.DEFENDING:
                self.energy -= 60
                self.saturation -= 20
                self.population -= 3
            case self.State.MULTIPLYING:
                self.population += 4
                self.energy -= 30
                self.saturation -= 20
            case self.State.ESCAPING:
                self.population -= 12
                self.energy -= 20
                self.saturation -= 10

    def get_output(self) -> dict[SharedParam, bool]:
        ip = self.internal_params
        pp = self.PrivateParam
        return {
            SharedParam.HERBIVORES_WILL_DEFEND: ip[pp.HAS_ENERGY_TO_DEFEND],
            SharedParam.HERBIVORES_AVAILABLE: self.population > self.config[self.Config.AVAILABILITY_THRESHOLD],
        }
