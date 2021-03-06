from typing import Set

import crowns.cards as cards
import crowns.decision as decision
import crowns.scoring as scoring
from crowns.cards import Card

def simulate(hand: Set[Card], wilds: int):
    unsorted = cards.all_except(
        hand_size=len(hand) + wilds,
        hand=hand
    )

    draws = cards.sort(unsorted)

    scenarios = []
    for draw in draws:
        temp_hand = hand.union([draw])
        discard = decision.choose_discard(temp_hand, wilds)
        scoring_hand = temp_hand.difference([discard])
        configuration = scoring.find_best_configuration(scoring_hand, wilds)

        scenarios.append((draw, configuration))

    wild_discard = decision.choose_discard(hand, wilds + 1)
    wild_scoring_hand = hand.difference([wild_discard])
    wild_configuration = scoring.find_best_configuration(wild_scoring_hand, wilds + 1)
    wild_score = wild_configuration.score

    wilds_remaining = cards.TotalWilds - wilds
    expected_score = (
        sum(scenario[1].score for scenario in scenarios)
        + wild_score * wilds_remaining
    ) / (len(scenarios) + wilds_remaining)

    scores = [wild_score] * wilds_remaining
    for _, configuration in scenarios:
        scores.append(configuration.score)

    return {
        "scenarios": scenarios,
        "expected_score": expected_score,
        "wild_configuration": wild_configuration,
        "scores": scores,
    }
