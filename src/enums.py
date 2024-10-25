from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def values(cls):
        return [value.value for value in cls.__members__.values()]


class Sex(BaseEnum):
    MALE="male"
    FEMALE="female"


class Mode(BaseEnum):
    ZERO=0
    ONE=1
    TWO=2
    THREE=3
    FOUR=4
    FIVE=5
    SIX=6
