import unittest

from crowns.decision import choose_discard
from tests.test_helpers import *

class TestChooseDiscard_basic(unittest.TestCase):
    def test_basic(self):
        discard = choose_discard(set([H3, C3, S3, S4]), 0)
        self.assertEqual(discard, S4)

    def test_basic_with_wildcard(self):
        discard = choose_discard(set([H3, C4, S5, S6]), 1)
        self.assertEqual(discard, C4)

