from collections import namedtuple
from enum import IntEnum, Enum, auto
from functools import total_ordering

class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(Enum):
    SPADE = auto()
    HEART = auto()
    DIAMOND = auto()
    CLUB = auto()


@total_ordering
class Card(namedtuple('Card', ['rank', 'suit'])):
    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank
