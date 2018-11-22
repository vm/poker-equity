from models import Rank


def test_rank_order():
    assert Rank.TWO < Rank.ACE
    assert Rank.ACE == Rank.ACE
    assert Rank.JACK < Rank.KING
