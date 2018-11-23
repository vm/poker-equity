from collections import Counter
from enum import IntEnum, Enum, auto
from functools import total_ordering
import operator

from funcy import lmap, lsplit


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
    THREE_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_KIND = 8
    STRAIGHT_FLUSH = 9


class Hand:
    def __init__(self, cards):
        straight = self._is_straight(cards)
        flush = self._is_flush(cards)
        if straight and flush:
            self.category = HandCategory.STRAIGHT_FLUSH
            self.involved, self.kickers = straight
            return

        four_kind = self._is_four_kind(cards)
        if four_kind:
            self.category = HandCategory.FOUR_KIND
            self.involved, self.kickers = four_kind
            return

        full_house = self._is_full_house(cards)
        if full_house:
            self.category = HandCategory.FULL_HOUSE
            self.involved, self.kickers = full_house

        if flush:
            self.category = HandCategory.FLUSH
            self.involved, self.kickers = flush
            return

        if straight:
            self.category = HandCategory.STRAIGHT
            self.involved, self.kickers = straight
            return

        three_kind = self._is_three_kind(cards)
        if three_kind:
            self.category = HandCategory.THREE_KIND
            self.involved, self.kickers = three_kind
            return

        two_pair = self._is_two_pair(cards)
        if two_pair:
            self.category = HandCategory.TWO_PAIR
            self.involved, self.kickers = two_pair
            return

        one_pair = self._is_one_pair(cards)
        if one_pair:
            self.category = HandCategory.ONE_PAIR
            self.involved, self.kickers = one_pair
            return

        high_card = self._is_high_card(cards)
        self.category = HandCategory.HIGH_CARD
        self.involved, self.kickers = high_card
        return

    def __eq__(self, other):
        return (
            self.category == other.category and
            self.involved == other.involved and
            self.kickers == other.kickers
        )

    @staticmethod
    def _operation(h1, h2, operand):
        if operand(h1.category, h2.category):
            return True
        for i1, i2 in zip(h1.involved, h2.involved):
            if i1 != i2:
                return operand(i1, i2)
        for k1, k2 in zip(h1.kickers, h2.kickers):
            if k1 != k2:
                return operand(k1, k2)
        return False

    def __lt__(self, other):
        return self._operation(self, other, operator.lt)

    def __le__(self, other):
        return self._operation(self, other, operator.le)

    def __gt__(self, other):
        return self._operation(self, other, operator.gt)

    def __ge__(self, other):
        return self._operation(self, other, operator.ge)

    @staticmethod
    def _get_ranks(cards):
        return lmap(operator.attrgetter('rank'), cards)

    @staticmethod
    def _get_suits(cards):
        return lmap(operator.attrgetter('suit'), cards)

    @classmethod
    def _is_flush(cls, cards):
        suits = cls._get_suits(cards)
        if len(set(suits)) == 1:
            return cards, []
        return None

    @classmethod
    def _is_full_house(cls, cards):
        ordered_ranks = Counter(cls._get_ranks(cards)).most_common()
        top_rank, top_count = ordered_ranks[0]
        bottom_rank, bottom_count = ordered_ranks[1]
        if top_count == 3 and bottom_count == 2:
            return lsplit(lambda c: c.rank in {top_rank, bottom_rank}, cards)
        return None

    @classmethod
    def _is_two_pair(cls, cards):
        ordered_ranks = Counter(cls._get_ranks(cards)).most_common()
        top_rank, top_count = ordered_ranks[0]
        bottom_rank, bottom_count = ordered_ranks[1]
        if top_count == 2 and bottom_count == 2:
            return lsplit(lambda c: c.rank in {top_rank, bottom_rank}, cards)
        return None

    @classmethod
    def _is_one_pair(cls, cards):
        ordered_ranks = Counter(cls._get_ranks(cards)).most_common()
        top_rank, top_count = ordered_ranks[0]
        bottom_rank, bottom_count = ordered_ranks[1]
        if top_count == 2:
            return lsplit(lambda c: c.rank in {top_rank, bottom_rank}, cards)
        return None

    @classmethod
    def _is_three_kind(cls, cards):
        ordered_ranks = Counter(cls._get_ranks(cards)).most_common()
        top_rank, top_count = ordered_ranks[0]
        if top_count == 3:
            return lsplit(lambda c: c.rank == top_rank, cards)
        return None

    @classmethod
    def _is_four_kind(cls, cards):
        ordered_ranks = Counter(cls._get_ranks(cards)).most_common()
        top_rank, top_count = ordered_ranks[0]
        if top_count == 4:
            return lsplit(lambda c: c.rank == top_rank, cards)
        return None

    @classmethod
    def _is_straight(cls, cards):
        # doesn't handle low A
        ranks = cls._get_ranks(cards)
        if (len(set(ranks)) == HAND_SIZE and
                max(ranks) - min(ranks) == HAND_SIZE - 1):
            return cards, []
        return None

    @classmethod
    def _is_high_card(cls, cards):
        return [], cards
