from flask import Flask
from flask import render_template

import crowns.cards as cards
import crowns.decision as decision
import crowns.game.dealer as dealer
import crowns.scoring as scoring
import crowns.simulation as simulation
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
        Suit.Spades: '<span class="spades">&spades;</span>',
        Suit.Hearts: '<span class="hearts">&hearts;</span>',
        Suit.Clubs: '<span class="clubs">&clubs;</span>',
        Suit.Diamonds: '<span class="diamonds">&diams;</span>',
        Suit.Stars: '<span class="stars">&#9733;</span>',
    }

    return f"{ranks[card.rank]}{suits[card.suit]}"

@app.route('/')
def hello_world():
    hand_size = 4
    wilds = 1
    hand = dealer.deal(hand_size, hand_size - wilds)

    current_score = scoring.find_best_configuration(hand, wilds).score

    simulated = simulation.simulate(hand, wilds)

    game = {
        "hand": [
            card_to_fragment(card)
            for card in cards.sort(hand)
        ],
        "wilds": wilds,
        "scenarios": [
            (
                card_to_fragment(draw),
                [
                    card_to_fragment(card)
                    for card in cards.sort(scoring_hand)
                ],
                score
            )
            for draw, scoring_hand, score
            in simulated["scenarios"]
        ],
        "wild_scoring_hand": [
            card_to_fragment(card)
            for card in cards.sort(simulated["wild_scoring_hand"])
        ],
        "wild_score": simulated["wild_score"],
        "expected_score": simulated["expected_score"],
        "current_score": current_score
    }

    return render_template('index.html', title='Five Crowns: Hand Analyzer', game=game)

if __name__ == '__main__':
    app.run()
