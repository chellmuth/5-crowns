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
