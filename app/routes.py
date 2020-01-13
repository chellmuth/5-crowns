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
    if card == "*": return "*"

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

def configuration_view(configuration):
    return {
        "score": configuration.score,
        "matches": [
            [
                card_to_fragment(card)
                for card in cards.sort(match.cards)
            ] + [ "*" for _ in range(match.wilds) ]
            for match in configuration.matches
        ],
        "remaining": [ card_to_fragment(card) for card in configuration.remaining ]
    }


@app.route('/')
def hello_world():
    hand_size = 3
    wilds = 0
    hand = dealer.deal(hand_size, hand_size - wilds)

    current_configuration = scoring.find_best_configuration(hand, wilds)

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
                configuration_view(configuration),
                configuration.score
            )
            for draw, configuration
            in simulated["scenarios"]
        ],
        "wild_configuration": configuration_view(simulated["wild_configuration"]),
        "expected_score": simulated["expected_score"],
        "current_configuration": configuration_view(current_configuration),
        "current_score": current_configuration.score,
    }

    return render_template('index.html', title='Five Crowns: Hand Analyzer', game=game)

if __name__ == '__main__':
    app.run()
