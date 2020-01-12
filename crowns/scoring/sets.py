from crowns.scoring.match import Match

import itertools

def find_sets(base, hand, wilds, size):
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

