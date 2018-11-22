from operator import attrgetter

from funcy import lmap

from models import Rank, Suit, Card


def test_rank_order():
    assert Rank.TWO < Rank.ACE
    assert Rank.KING > Rank.JACK
    assert Rank.ACE == Rank.ACE


def test_card_order():
    assert Card(Rank.TWO, Suit.SPADE) < Card(Rank.ACE, Suit.SPADE)
    assert Card(Rank.ACE, Suit.SPADE) == Card(Rank.ACE, Suit.HEART)
    assert Card(Rank.KING, Suit.SPADE) > Card(Rank.JACK, Suit.HEART)


def test_card_sort_same_suit():
    cards = [
        Card(Rank.TWO, Suit.SPADE),
        Card(Rank.ACE, Suit.SPADE),
        Card(Rank.KING, Suit.SPADE),
    ]
    assert lmap(attrgetter('rank'), sorted(cards, reverse=True)) == [Rank.ACE, Rank.KING, Rank.TWO]
