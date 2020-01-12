import unittest

from crowns.scoring.match import Match
from crowns.scoring.runs import find_runs
from tests.test_helpers import *

class TestFindRuns_size_three__basic_matches(unittest.TestCase):
    def test_no_wilds(self):
        hand = set([S4, S5])

        matches = find_runs(S3, hand, wilds=0, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3, S4, S5]), set(), 0)
            ]
        )

    def test_one_card_two_wilds(self):
        hand = set([S4, S5])

        matches = find_runs(S3, hand, wilds=2, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3]), set([S4, S5]), 2)
            ]
        )

    def test_two_options__one_wild(self):
        hand = set([S4, S5])

        matches = find_runs(S3, hand, wilds=1, size=3)

        self.assertEqual(
            matches,
            [
                Match(set([S3, S4]), set([S5]), 1),
                Match(set([S3, S5]), set([S4]), 1)
            ]
        )

