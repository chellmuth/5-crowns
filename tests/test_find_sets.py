import unittest

from crowns.scoring.match import Match
from crowns.scoring.sets import find_sets
from crowns.cards import Card, Suit, Rank

H3 = Card(Suit.Hearts, Rank.Three)
C3 = Card(Suit.Clubs, Rank.Three)
S3 = Card(Suit.Spades, Rank.Three)

S4 = Card(Suit.Spades, Rank.Four)
S5 = Card(Suit.Spades, Rank.Five)

class TestFindSets_size_three__basic_matches(unittest.TestCase):
    def test_no_wilds(self):
        hand = set([H3, C3])

        matches = find_sets(S3, hand, wilds=0, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([H3, C3, S3]), set(), 0)
            ]
        )

    def test_one_card_two_wilds(self):
        hand = set([H3, C3])

        matches = find_sets(S3, hand, wilds=2, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3]), set([H3, C3]), 2)
            ]
        )

    def test_two_options__one_wild(self):
        hand = set([H3, C3])

        matches = find_sets(S3, hand, wilds=1, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3, H3]), set([C3]), 1),
                Match(set([S3, C3]), set([H3]), 1)
            ]
        )

    def test_empty_with_too_many_wilds(self):
        hand = set([H3, C3])

        matches = find_sets(S3, hand, wilds=3, size=3)

        self.assertEqual(matches, [])

class TestFindSets_size_three__basic_different_ranks(unittest.TestCase):
    def test_no_wilds(self):
        hand = set([S4, S5])

        matches = find_sets(S3, hand, wilds=0, size=3)

        self.assertEqual(matches, [])

    def test_one_wild(self):
        hand = set([S4, S5])

        matches = find_sets(S3, hand, wilds=1, size=3)

        self.assertEqual(matches, [])

    def test_two_wilds(self):
        hand = set([S4, S5])

        matches = find_sets(S3, hand, wilds=2, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3]), hand, 2)
            ]
        )

