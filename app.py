from flask import Flask

import crowns.cards as cards
import crowns.decision as decision
import crowns.game.dealer as dealer
import crowns.scoring as scoring

app = Flask(__name__)

@app.route('/')
def hello_world():
    hand = dealer.deal(3)
    score = scoring.find_best_configuration(hand, 0).score

    draws = cards.all_except(hand)

    scenarios = []
    for draw in draws:
        temp_hand = hand.union([draw])
        discard = decision.choose_discard(temp_hand, 0)
        scoring_hand = temp_hand.difference([discard])
        score = scoring.find_best_configuration(scoring_hand, 0).score

        scenarios.append((draw, scoring_hand, score))

    return str(hand) + " " + str(score) + " " + str(scenarios)

if __name__ == '__main__':
    app.run()
