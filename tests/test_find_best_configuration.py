import unittest

from crowns.scoring import find_best_configuration, HandConfiguration
from tests.test_helpers import *

class TestBestConfiguration_size_three__sets__no_wilds(unittest.TestCase):
    def test_set_of_three(self):
        best = find_best_configuration(set([H3, C3, S3]))
        self.assertEqual(best.score, 0)

    def test_no_match(self):
        best = find_best_configuration(set([H3, C3, S4]))
        self.assertEqual(best.score, 10)


class TestBestConfiguration_size_four__sets__no_wilds(unittest.TestCase):
    def test_set_of_four(self):
        best = find_best_configuration(set([H3, C3, S3, D3]))
        self.assertEqual(best.score, 0)

    def test_set_of_three(self):
        best = find_best_configuration(set([C4, H3, C3, S3]))
        self.assertEqual(best.score, 4)

    def test_no_match(self):
        best = find_best_configuration(set([H3, C3, S4, C4]))
        self.assertEqual(best.score, 14)


class TestBestConfiguration_two_sets__no_wilds(unittest.TestCase):
    def test_two_sets_of_three(self):
        best = find_best_configuration(set([H3, C3, S3, H4, C4, S4]))
        self.assertEqual(best.score, 0)

    def test_two_sets_of_different_sizes(self):
        best = find_best_configuration(set([H3, C3, S3, D3, H4, C4, S4]))
        self.assertEqual(best.score, 0)

    def test_two_sets_of_different_sizes__with_leftovers(self):
        best = find_best_configuration(set([H3, C3, S3, D3, H4, C4, S4, S5, C5]))
        self.assertEqual(best.score, 10)


class TestBestConfiguration_sets_and_runs__no_wilds(unittest.TestCase):
    def test_run_better_than_set(self):
        best = find_best_configuration(set([H3, C3, S3, S4, S5]))
        self.assertEqual(best.score, 6)

    def test_set_better_than_run(self):
        best = find_best_configuration(set([S4, S5, S6, C6, H6]))
        self.assertEqual(best.score, 9)
