from dataclasses import dataclass
from typing import Set

from crowns.cards import Card

@dataclass
class Match:
    cards: Set[Card]
    hand: Set[Card]
    wilds: int
