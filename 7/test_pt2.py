from pt2 import Hand, Card, HandRank


def test_hand_rank():
    hand = Hand([Card("A"), Card("K"), Card("Q"), Card("J"), Card("T")])
    assert hand.rank == HandRank.ONE_PAIR
    hand = Hand([Card("K"), Card("K"), Card("Q"), Card("J"), Card("T")])
    assert hand.rank == HandRank.THREE_OF_A_KIND
    hand = Hand([Card("K"), Card("K"), Card("Q"), Card("Q"), Card("T")])
    assert hand.rank == HandRank.TWO_PAIR
    hand = Hand([Card("K"), Card("K"), Card("J"), Card("J"), Card("T")])
    assert hand.rank == HandRank.FOUR_OF_A_KIND
    hand = Hand([Card("K"), Card("K"), Card("K"), Card("J"), Card("T")])
    assert hand.rank == HandRank.FOUR_OF_A_KIND
    hand = Hand([Card("K"), Card("K"), Card("K"), Card("J"), Card("J")])
    assert hand.rank == HandRank.FIVE_OF_A_KIND
    hand = Hand([Card("K"), Card("K"), Card("K"), Card("K"), Card("T")])
    assert hand.rank == HandRank.FOUR_OF_A_KIND
    hand = Hand([Card("K"), Card("K"), Card("K"), Card("K"), Card("K")])
    assert hand.rank == HandRank.FIVE_OF_A_KIND


def test_hand_rank_comparison():
    hand1 = Hand([Card("J"), Card("K"), Card("K"), Card("K"), Card("2")])
    hand2 = Hand([Card("Q"), Card("Q"), Card("Q"), Card("Q"), Card("2")])
    assert hand1 < hand2
    assert hand1 != hand2
    assert not (hand1 > hand2)
