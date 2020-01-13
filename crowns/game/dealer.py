import random

import crowns.game.deck as deck

class Dealer:
    def __init__(self, hand_size, wilds=True):
        self.hand_size = hand_size

        if wilds:
            self.deck = deck.Deck(self.hand_size)
        else:
            self.deck = deck.Deck(self.hand_size, wilds=0)

    def deal(self):
        return set(self.deck.deal())
