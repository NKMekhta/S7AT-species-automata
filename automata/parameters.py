from enum import Enum


class SharedParam(Enum):
    PREDATOR_EATING = 0
    PREDATOR_HUNTING_HERBIVORES = 1
    PREDATOR_HUNTING_SCAVENGERS = 2
    HERBIVORES_WILL_DEFEND = 3
    HERBIVORES_AVAILABLE = 4
