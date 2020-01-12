import unittest

from crowns.scoring.match import Match
from crowns.scoring.sets import find_sets
from tests.test_helpers import *

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

class TestFindSets_size_three__basic_one_pair(unittest.TestCase):
    def test_no_wilds(self):
        matches = find_sets(S3, set([C3, C4]), wilds=0, size=3)

        self.assertEqual(matches, [])

    def test_one_wild(self):
        matches = find_sets(S3, set([C3, C4]), wilds=1, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3, C3]), set([C4]), 1)
            ]
        )

    def test_two_wilds(self):
        matches = find_sets(S3, set([C3, C4]), wilds=2, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3]), set([C3, C4]), 2)
            ]
        )

class TestFindSets_size_three__basic_one_pair_off(unittest.TestCase):
    def test_no_wilds(self):
        matches = find_sets(C3, set([C4, S4]), wilds=0, size=3)

        self.assertEqual(matches, [])

    def test_one_wild(self):
        matches = find_sets(C3, set([C4, S4]), wilds=1, size=3)

        self.assertEqual(matches, [])

    def test_two_wilds(self):
        matches = find_sets(C3, set([C4, S4]), wilds=2, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([C3]), set([C4, S4]), 2)
            ]
        )
