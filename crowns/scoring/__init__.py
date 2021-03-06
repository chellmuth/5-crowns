from dataclasses import dataclass
from typing import List, Set

from crowns.cards import Card
from crowns.scoring.match import Match
from crowns.scoring.runs import find_runs
from crowns.scoring.sets import find_sets

@dataclass
class HandConfiguration:
    score: int
    matches: List[Match]
    remaining: List[Card]

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

def find_best_configuration(hand: Set[Card], wilds: int) -> HandConfiguration:
    return _find_best_configuration(hand, wilds, [])

def _find_best_configuration(
        hand: Set[Card],
        wilds: int,
        matches: List[Match]
) -> HandConfiguration:
    if not hand: return HandConfiguration(0, matches, hand)

    best_configuration = None

    match_queue = []
    for card in hand:
        rest = hand.difference([card])

        for wild in range(wilds + 1):
            for size in range(3, len(rest) + wild + 2):
                set_matches = find_sets(card, rest, wild, size)
                match_queue.extend(set_matches)

                run_matches = find_runs(card, rest, wild, size)
                match_queue.extend(run_matches)

    if not match_queue:
        return HandConfiguration(score(hand), matches, hand)

    for match in match_queue:
        best_configuration = _update_best_configuration(
            best_configuration,
            _find_best_configuration(
                match.hand,
                wilds - match.wilds,
                matches + [match]
            )
        )

    return best_configuration

def score(hand: Set[Card]) -> int:
    return sum(card.rank for card in hand)
