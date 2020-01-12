from flask import Flask
from flask import render_template

import crowns.cards as cards
import crowns.decision as decision
import crowns.game.dealer as dealer
import crowns.scoring as scoring
from crowns.cards import Rank, Suit

from app import app

def card_to_fragment(card):
    ranks = {
        Rank.Three: "3",
        Rank.Four: "4",
        Rank.Five: "5",
        Rank.Six: "6",
        Rank.Seven: "7",
        Rank.Eight: "8",
        Rank.Nine: "9",
        Rank.Ten: "T",
        Rank.Jack: "J",
        Rank.Queen: "Q",
        Rank.King: "K",
    }

    suits = {
        Suit.Spades: "&spades;",
        Suit.Hearts: "&hearts;",
        Suit.Clubs: "&clubs;",
        Suit.Diamonds: "&diams;",
        Suit.Stars: "&#9733;",
    }

    return f"{ranks[card.rank]}{suits[card.suit]}"

@app.route('/')
def hello_world():
    hand = dealer.deal(3)
    current_score = scoring.find_best_configuration(hand, 0).score

    draws = cards.all_except(hand)

    scenarios = []
    for draw in draws:
        temp_hand = hand.union([draw])
        discard = decision.choose_discard(temp_hand, 0)
        scoring_hand = temp_hand.difference([discard])
        score = scoring.find_best_configuration(scoring_hand, 0).score

        scenarios.append((draw, scoring_hand, score))


    old_result = str(hand) + " " + str(score) + " " + str(scenarios)

    game = {
        "hand": [
            card_to_fragment(card)
            for card in hand
        ],
        "scenarios": [
            (
                card_to_fragment(draw),
                [
                    card_to_fragment(card)
                    for card in scoring_hand
                ],
                score
            )
            for draw, scoring_hand, score
            in scenarios
        ],
        "current_score": current_score
    }

    return render_template('index.html', title='Five Crowns: Hand Analyzer', game=game)

if __name__ == '__main__':
    app.run()
