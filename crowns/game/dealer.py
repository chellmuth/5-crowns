import random

import crowns.game.deck as deck

class Dealer:
    def __init__(self, hand_size, include_wilds=True):
        self.hand_size = hand_size

        if include_wilds:
            self.deck = deck.Deck(self.hand_size)
        else:
            self.deck = deck.Deck(self.hand_size, wilds=0)

        self.fake_discard()

    def deal(self):
        return self.deck.deal()

    def draw(self, hand):
        drawn = self.deck.draw()
        if drawn:
            hand.append(drawn)

    def fake_discard(self):
        # No wilds in the discard for now
        drawn = None
        while drawn is None:
            drawn = self.deck.draw()

        self.discard = drawn
