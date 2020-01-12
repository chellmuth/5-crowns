from dataclasses import dataclass
from typing import List, Set

from crowns.cards import Card
from crowns.scoring.match import Match
from crowns.scoring.sets import find_sets

@dataclass
class HandConfiguration:
    score: int
    # matches: List[Match]

def _update_best_configuration(
    current_best: HandConfiguration,
    new_configuration: HandConfiguration
) -> HandConfiguration:

    if current_best is None:
        return new_configuration

    if new_configuration is None:
        return current_best

    if new_configuration.score < current_best.score:
        return new_configuration

    return current_best

def find_best_configuration(hand: Set[Card]) -> HandConfiguration:
    if not hand: return HandConfiguration(0)

    best_configuration = None

    for card in hand:
        rest = hand.difference([card])

        matches = find_sets(card, rest, wilds=0, size=3)
        if not matches:
            return HandConfiguration(score(hand))

        for match in matches:
            best_configuration = _update_best_configuration(
                best_configuration,
                find_best_configuration(match.hand)
            )

    return best_configuration

def score(hand: Set[Card]) -> int:
    return sum(card.rank for card in hand)
