import random

import crowns.cards as cards

class Deck:
    def __init__(self, hand_size, wilds=cards.TotalWilds):
        self.hand_size = hand_size
        self.wilds = wilds

        unshuffled = cards.all(self.hand_size)
        random.shuffle(unshuffled)

        self.shuffled = unshuffled

    def deal(self):
        cards = []

        for _ in range(self.hand_size):
            wild_odds = self.wilds / (len(self.shuffled) + self.wilds)
            if random.random() > wild_odds:
                cards.append(self.shuffled.pop())
            else:
                self.wilds -= 1

        return cards
