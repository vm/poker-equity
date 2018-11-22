from collections import Counter
from enum import IntEnum, Enum, auto
from functools import total_ordering
from operator import ne, lt, attrgetter

from funcy import lmap


HAND_SIZE = 5

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
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __hash__(self):
        return hash(tuple(self))


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
class Hand:
    def __init__(self, category, cards):
        self.category = category
        self.cards = cards

    def __eq__(self, other):
        return (
            self.category == other.category or
            all(map(lambda x: ne(*x), zip(self.cards, other.cards)))
        )

    def __lt__(self, other):
        return (
            self.category < other.category or
            all(map(lambda x: lt(*x), zip(self.cards, other.cards)))
        )

    @property
    def _ranks(self):
        return lmap(attrgetter('rank'), self.cards)

    @property
    def _suits(self):
        return lmap(attrgetter('suit'), self.cards)

    def _is_straight(self):
        # doesn't handle low A
        return (len(set(self._ranks)) == HAND_SIZE and
            max(self._ranks) - min(self._ranks) == HAND_SIZE - 1
        )

    def _is_flush(self):
        suit_counter = Counter(self._suits)
        suit, count = suit_counter.most_common()[0]
        return count >= HAND_SIZE
