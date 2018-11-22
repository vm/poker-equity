from models import Rank, Suit, Card


def test_rank_order():
    assert Rank.TWO < Rank.ACE
    assert Rank.KING > Rank.JACK
    assert Rank.ACE == Rank.ACE


def test_card_order():
    assert Card(Rank.TWO, Suit.SPADE) < Card(Rank.ACE, Suit.SPADE)
    assert Card(Rank.ACE, Suit.SPADE) == Card(Rank.ACE, Suit.HEART)
    assert Card(Rank.KING, Suit.SPADE) > Card(Rank.JACK, Suit.HEART)
