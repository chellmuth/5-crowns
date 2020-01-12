# import itertools
# from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from typing import List

class Suit(IntEnum):
    Spades = 1
    Hearts = 2
    Clubs = 3
    Diamonds = 4
    Stars = 5

class Rank(IntEnum):
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

@dataclass(eq=True, frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def encoded_id(self):
        return (self.rank - 3) * 5 + (self.suit - 1)

    def __repr__(self):
        return f"({self.suit}, {self.rank})"

# @dataclass
# class Hand:
#     cards: List[Card]

#     def add_card(self, card):
#         self.cards.append(card)

#     def encoded(self):
#         encoded = np.zeros((11 * 5,))
#         for card in self.cards:
#             encoded[card.encoded_id()] = 1

#         return encoded

#     def discard_ids(self):
#         return [
#             card.encoded_id()
#             for card in self.cards
#         ]

#     def discard(self, card):
#         self.cards.remove(card)
#         return card

#     def discard_highest(self):
#         ranked = sorted(self.cards, key=lambda card: card.rank)
#         self.cards.remove(ranked[-1])

#     def unpaired_cards(self):
#         rank_counts = Counter()
#         for card in self.cards:
#             rank_counts[card.rank] += 1

#         return [
#             card
#             for card in self.cards
#             if rank_counts[card.rank] <= 1
#         ]

#     def __repr__(self):
#         return ", ".join([
#             str(card) for card in self.cards
#         ])

# def highest_card(cards):
#     return sorted(cards, key=lambda card: (card.rank, card.suit))[-1]

# def card_by_id(card_id):
#     return Card(Suit(card_id % 5 + 1), Rank(card_id // 5 + 3), False)

# def init_deck():
#     unshuffled = [
#         Card(*card, False)
#         for card
#         in itertools.product(Suit, Rank)
#     ]

#     return unshuffled
