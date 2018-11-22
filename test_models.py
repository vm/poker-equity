from operator import attrgetter

from funcy import lmap

from models import Rank, Suit, Card, Hand, HandCategory


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


def test_hand_order():
    card1 = Card(Rank.TWO, Suit.SPADE)
    card2 = Card(Rank.THREE, Suit.SPADE)
    card3 = Card(Rank.TEN, Suit.SPADE)
    card4 = Card(Rank.KING, Suit.SPADE)
    card5 = Card(Rank.ACE, Suit.SPADE)
    card6 = Card(Rank.ACE, Suit.HEART)

    hand1 = Hand(HandCategory.HIGH_CARD, [card1, card2, card3, card4, card5])
    hand2 = Hand(HandCategory.HIGH_CARD, [card1, card2, card3, card4, card5])
    hand3 = Hand(HandCategory.ONE_PAIR, [card1, card2, card3, card5, card6])

    assert hand1 == hand2
    assert hand1 < hand3
