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
