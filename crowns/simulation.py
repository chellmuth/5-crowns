from typing import Set

import crowns.cards as cards
import crowns.decision as decision
import crowns.scoring as scoring
from crowns.cards import Card

def simulate(hand: Set[Card], wilds: int):
    draws = cards.sort(cards.all_except(hand))

    scenarios = []
    for draw in draws:
        temp_hand = hand.union([draw])
        discard = decision.choose_discard(temp_hand, wilds)
        scoring_hand = temp_hand.difference([discard])
        score = scoring.find_best_configuration(scoring_hand, wilds).score

        scenarios.append((draw, scoring_hand, score))

    expected_score = sum(scenario[2] for scenario in scenarios) / len(scenarios)

    return {
        "scenarios": scenarios,
        "expected_score": expected_score
    }
