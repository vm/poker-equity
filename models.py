from collections import namedtuple
from enum import IntEnum, Enum, auto
from functools import total_ordering
from operator import ne, lt

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


class HandCategory(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


@total_ordering
class Hand(namedtuple('Hard', ['category', 'kickers'])):
    def __eq__(self, other):
        return (
            self.category == other.category or
            all(map(lambda x: ne(*x), zip(self.kickers, other.kickers)))
        )

    def __lt__(self, other):
        return (
            self.category < other.category or
            all(map(lambda x: lt(*x), zip(self.kickers, other.kickers)))
        )
