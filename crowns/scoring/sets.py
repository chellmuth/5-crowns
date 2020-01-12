import itertools
from typing import Set

from crowns.cards import Card
from crowns.scoring.match import Match

def find_sets(base: Card, hand: Set[Card], wilds: int, size: int):
    if wilds >= size: return []

    same_ranks = []

    for card in hand:
        if base.rank == card.rank:
            same_ranks.append(card)

    combinations = itertools.combinations(same_ranks, size - wilds - 1)
    matches = []
    for combination in combinations:
        match = Match(
            set(combination).union([base]),
            set(hand) - set(combination),
            wilds
        )
        matches.append(match)

    return matches

