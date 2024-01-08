from enum import Enum
from typing import Any

from .parameters import SharedParam


class Scavenger:
    class Config(Enum):
        INITIAL_POPULATION = 1
        INITIAL_SATURATION = 2
        INITIAL_ENERGY = 3
        INITIAL_STATE = 4
        POPULATION_LIMIT = 5

    class State(Enum):
        CANNIBALISM = 0
        WANDERING = 1
        EATING = 2
        SLEEPING = 3
        MULTIPLYING = 4
        HIDING = 5

    class PrivateParam(Enum):
        SHOULD_SLEEP = 1
        STARVING = 2
        SHOULD_MULTIPLY = 3
        FULL = 4

    config: dict[Config, Any] = {
        Config.INITIAL_SATURATION: 100,
        Config.INITIAL_POPULATION: 10,
        Config.INITIAL_ENERGY: 100,
        Config.INITIAL_STATE: State.SLEEPING,
        Config.POPULATION_LIMIT: 50,
    }

    def __init__(self):
        self.population: int = self.config[self.Config.INITIAL_POPULATION]
        self.saturation: int = self.config[self.Config.INITIAL_SATURATION]
        self.energy: int = self.config[self.Config.INITIAL_ENERGY]
        self.state: Scavenger.State = self.config[self.Config.INITIAL_STATE]
        self.internal_params: dict[Scavenger.PrivateParam, bool] = {}
        self.__update_internals()

    def update(self, input_params: dict[SharedParam, bool]):
        self.__update_internals()
        ip = self.internal_params
        pp = self.PrivateParam
        sp = SharedParam
        st = self.State
        routine_state = {
            ip[pp.SHOULD_SLEEP]: st.SLEEPING,
            ip[pp.SHOULD_MULTIPLY]: st.MULTIPLYING
        }.setdefault(True, st.WANDERING)

        match self.state:
            case st.MULTIPLYING | st.SLEEPING | st.WANDERING:
                if input_params[sp.PREDATOR_HUNTING_SCAVENGERS]:
                    self.state = st.HIDING
                elif input_params[sp.PREDATOR_EATING] and not ip[pp.FULL]:
                    self.state = st.EATING
                elif not input_params[sp.PREDATOR_EATING] and ip[pp.STARVING]:
                    self.state = st.CANNIBALISM
                else:
                    self.state = routine_state
            case st.CANNIBALISM:
                if input_params[sp.PREDATOR_EATING]:
                    self.state = st.EATING
                else:
                    self.state = routine_state
            case st.EATING:
                self.state = routine_state
            case st.HIDING:
                self.state = st.EATING
        self.__update_variables()

    def __update_internals(self):
        ip = self.internal_params
        pp = self.PrivateParam
        ip[pp.STARVING] = self.saturation <= 0
        ip[pp.FULL] = self.saturation >= 80
        ip[pp.SHOULD_SLEEP] = self.energy < 10
        ip[pp.SHOULD_MULTIPLY] = self.energy >= 30 and 60 <= self.saturation
        self.internal_params = ip

    def __update_variables(self):
        match self.state:
            case self.State.EATING:
                self.saturation += 60
            case self.State.SLEEPING:
                self.energy += 70
                self.saturation -= 10
            case self.State.HIDING:
                self.energy -= 20
                self.saturation -= 10
                self.population -= 6
            case self.State.CANNIBALISM:
                self.saturation += 40
                self.population -= 2
            case self.State.MULTIPLYING:
                self.population += 8
                self.energy -= 30
                self.saturation -= 30
            case self.State.WANDERING:
                self.energy -= 10
                self.saturation -= 10

    def get_output(self) -> dict[SharedParam, bool]:
        return {}
