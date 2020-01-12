from typing import Set

from crowns.scoring import find_best_configuration
from crowns.cards import Card

def choose_discard(hand: Set[Card], wilds: int) -> Card:
    configurations = []
    for card in hand:
        rest = hand.difference([card])
        configurations.append((card, find_best_configuration(rest, wilds)))

    discard, _ = min(configurations, key=lambda bundle: bundle[1].score)
    return discard
