import itertools
from typing import Set

from crowns.cards import Card
from crowns.scoring.match import Match

# Find all runs that meet the following criteria:
#   1) Start with `base` (ie lowest rank)
#   2) Are exactly length `size`
#   3) Use exactly `wild` wilds
#   4) Only include cards in `hand`
def find_runs(base: Card, hand: Set[Card], wilds: int, size: int):
    if wilds >= size: return []

    runners = []
    wilds_remaining = wilds
    for i in range(size - 1):
        card = Card(base.suit, base.rank + i + 1)
        if card in hand:
            runners.append(card)
        else:
            wilds_remaining -= 1

        if wilds_remaining < 0:
            return []

    combinations = itertools.combinations(runners, size - wilds - 1)
    matches = []
    for combination in combinations:
        match = Match(
            set(combination).union([base]),
            set(hand) - set(combination),
            wilds
        )
        matches.append(match)

    return matches

