from operator import attrgetter

from funcy import lmap

from models import Rank, Suit, Card, Hand


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
    assert lmap(
        attrgetter('rank'),
        sorted(cards, reverse=True)) == [Rank.ACE, Rank.KING, Rank.TWO]


def test_hand_one_pair_equal():
    card1 = Card(Rank.TWO, Suit.SPADE)
    card2 = Card(Rank.THREE, Suit.HEART)
    card3 = Card(Rank.TEN, Suit.SPADE)
    card4 = Card(Rank.KING, Suit.CLUB)
    card5 = Card(Rank.ACE, Suit.SPADE)
    card6 = Card(Rank.ACE, Suit.HEART)

    hand1 = Hand([card1, card2, card3, card4, card5])
    hand2 = Hand([card1, card2, card3, card4, card5])
    hand3 = Hand([card1, card2, card3, card4, card6])

    assert hand1 == hand2
    assert hand1 == hand3


def test_hand_flush_vs_one_pair():
    card1 = Card(Rank.TWO, Suit.SPADE)
    card2 = Card(Rank.THREE, Suit.SPADE)
    card3 = Card(Rank.TEN, Suit.SPADE)
    card4 = Card(Rank.KING, Suit.SPADE)
    card5 = Card(Rank.ACE, Suit.SPADE)
    card6 = Card(Rank.ACE, Suit.HEART)

    hand1 = Hand([card1, card2, card3, card4, card5])
    hand2 = Hand([card1, card2, card3, card5, card6])

    assert hand1 > hand2


def test_hand_high_full_house_vs_low_full_house():
    card1 = Card(Rank.TWO, Suit.CLUB)
    card2 = Card(Rank.TWO, Suit.SPADE)
    card3 = Card(Rank.TWO, Suit.HEART)
    card4 = Card(Rank.KING, Suit.CLUB)
    card5 = Card(Rank.KING, Suit.SPADE)
    card6 = Card(Rank.KING, Suit.HEART)

    hand1 = Hand([card1, card2, card3, card4, card5])
    hand2 = Hand([card1, card2, card4, card5, card6])

    assert hand1 < hand2


def test_hand_non_top_high_card():
    card1 = Card(Rank.TWO, Suit.CLUB)
    card2 = Card(Rank.THREE, Suit.SPADE)
    card3 = Card(Rank.FOUR, Suit.HEART)
    card4 = Card(Rank.FIVE, Suit.CLUB)
    card5 = Card(Rank.SIX, Suit.CLUB)
    card6 = Card(Rank.KING, Suit.SPADE)

    hand1 = Hand([card1, card2, card3, card4, card6])
    hand2 = Hand([card1, card2, card3, card5, card6])

    assert hand1 < hand2


def test_hand_is_flush():
    card1 = Card(Rank.TWO, Suit.SPADE)
    card2 = Card(Rank.THREE, Suit.SPADE)
    card3 = Card(Rank.TEN, Suit.SPADE)
    card4 = Card(Rank.KING, Suit.SPADE)
    card5 = Card(Rank.ACE, Suit.SPADE)
    card6 = Card(Rank.ACE, Suit.HEART)

    assert Hand._is_flush([card1, card2, card3, card4, card5])
    assert not Hand._is_flush([card1, card2, card3, card5, card6])


def test_hand_is_straight():
    card1 = Card(Rank.TEN, Suit.SPADE)
    card2 = Card(Rank.JACK, Suit.SPADE)
    card3 = Card(Rank.THREE, Suit.SPADE)
    card4 = Card(Rank.KING, Suit.SPADE)
    card5 = Card(Rank.ACE, Suit.SPADE)
    card6 = Card(Rank.QUEEN, Suit.SPADE)

    assert Hand._is_straight([card1, card2, card4, card5, card6])
    assert not Hand._is_straight([card1, card2, card3, card4, card5])


def test_hand_is_three_kind():
    card1 = Card(Rank.TEN, Suit.SPADE)
    card2 = Card(Rank.TEN, Suit.HEART)
    card3 = Card(Rank.TEN, Suit.CLUB)
    card4 = Card(Rank.JACK, Suit.SPADE)
    card5 = Card(Rank.THREE, Suit.CLUB)
    card6 = Card(Rank.QUEEN, Suit.SPADE)

    assert Hand._is_three_kind([card1, card2, card3, card4, card5])
    assert not Hand._is_three_kind([card2, card3, card4, card5, card6])


def test_hand_is_four_kind():
    card1 = Card(Rank.TEN, Suit.SPADE)
    card2 = Card(Rank.TEN, Suit.HEART)
    card3 = Card(Rank.TEN, Suit.CLUB)
    card4 = Card(Rank.TEN, Suit.DIAMOND)
    card5 = Card(Rank.JACK, Suit.SPADE)
    card6 = Card(Rank.THREE, Suit.CLUB)

    assert Hand._is_four_kind([card1, card2, card3, card4, card5])
    assert not Hand._is_four_kind([card2, card3, card4, card5, card6])


def test_hand_is_full_house():
    card1 = Card(Rank.TEN, Suit.SPADE)
    card2 = Card(Rank.TEN, Suit.HEART)
    card3 = Card(Rank.TEN, Suit.CLUB)
    card4 = Card(Rank.JACK, Suit.DIAMOND)
    card5 = Card(Rank.JACK, Suit.SPADE)
    card6 = Card(Rank.THREE, Suit.CLUB)

    assert Hand._is_full_house([card1, card2, card3, card4, card5])
    assert not Hand._is_full_house([card1, card2, card3, card4, card6])
