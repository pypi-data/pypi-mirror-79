from enum import Enum, auto

class Policy(Enum):
    always = auto()
    unless_error = auto()
    never = auto()
